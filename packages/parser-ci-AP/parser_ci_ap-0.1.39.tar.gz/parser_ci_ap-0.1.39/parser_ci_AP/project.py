from pathlib import Path
from typing import List
import pickle

from .logger import logger
from .project_file import AbstractProjectFile, ProjectFile
from .type_info import BaseTypeInfo, StructInfo, UnionInfo, EnumInfo, TypedefInfo
from .function_info import FunctionInfo
from .variable_info import VariableInfo
from .define_info import DefineInfo
from .errors_info import DiagnosticInfo

class Project:
    def __init__(self, root_path: Path, file_class=ProjectFile):
        self.root_path: Path = root_path.resolve()
        self.files: List[AbstractProjectFile] = []
        self._file_class = file_class
        self.types: List[BaseTypeInfo] = []
        self.functions: List[FunctionInfo] = []
        self.variables: List[VariableInfo] = []

        logger.info(f"Инициализация проекта: {self.root_path}")
        self._parse_project()
        self.analyze_files_with_clang()
        self.types = self.all_types
        self.functions = self.global_functions + self.static_functions
        self.variables = self.global_variables + self.static_variables

        # Дополнительно находим макросы, которые использует та или иная функция
        for func in self.global_functions:
            func.extract_used_macros(self.all_user_defined)

    @staticmethod
    def get_picklable_copy(obj):
        for file in obj.files:
            file.get_picklable_copy(file)

        for func in obj.functions:
            func.get_picklable_copy(func)

        for t in obj.types:
            t.get_picklable_copy(t)

        for vr in obj.variables:
            vr.get_picklable_copy(vr)

    @staticmethod
    def save_obj(obj, save_path):
        # 1. Для сохранения объекта в файл (например для отладки так как этот объект считается очень долго) нужно
        # удалить все зависимости от ctype
        Project.get_picklable_copy(obj)

        # 2. Сохраняем объект используя библиотеку pickle
        with open(save_path, "wb") as f:
            pickle.dump(obj, f)

    @staticmethod
    def load_obj(load_path) -> "Project":
        # 1. Загружаем объект используя pickle
        with open(load_path, "rb") as f:
            obj = pickle.load(f)
        return obj

    def analyze_files_with_clang(self):
        """
        Вызывает clang-анализ для всех файлов
        """
        logger.debug("Анализ всех файлов через Clang")
        for pf in self.files:
            logger.debug(f"Анализ файла: {pf.path}")
            pf.analyze_with_clang()

    def _parse_project(self):
        """
        Находит и парсит все исходные файлы в проекте при инициализации.
        """
        logger.info("Поиск и анализ файлов проекта")
        for path in self.root_path.rglob("*"):
            if path.suffix in {".h"} and path.is_file():
                logger.debug(f"Найден заголовочный файл: {path}")
                pf = self._file_class(path, self.root_path)
                self.files.append(pf)

        for path in self.root_path.rglob("*"):
            if path.suffix in {".c"} and path.is_file():
                logger.debug(f"Найден исходный файл: {path}")
                pf = self._file_class(path, self.root_path)
                self.files.append(pf)

        # Находим все зависимости include для файлов .с
        self._resolve_all_includes()

    def _resolve_all_includes(self):
        """
        Для каждого файла в проекте собирает все включаемые файлы (прямо и косвенно),
        и устанавливает их с помощью _collect_all_includes_recursively.
        """
        logger.debug("Сбор всех #include зависимостей")
        # Словарь: имя файла -> список ProjectFile с таким именем
        name_to_files: dict[str, list[AbstractProjectFile]] = {}
        for pf in self.files:
            name_to_files.setdefault(pf.path.name, []).append(pf)

        for pf in self.files:
            visited: set[Path] = set()
            result: set[Path] = set()

            def recurse(include_name: str):
                # Проверяем все ProjectFile с таким именем
                for inc_pf in name_to_files.get(include_name, []):
                    inc_path = inc_pf.path.resolve()
                    if inc_path in visited:
                        continue
                    visited.add(inc_path)
                    result.add(inc_path)
                    for sub_include in inc_pf.includes:
                        recurse(sub_include)

            for direct_include in pf.includes:
                recurse(direct_include)

            # Устанавливаем все зависимости через метод
            pf.collect_all_includes_recursively(result)

    def extract_context_for_function(self, func: FunctionInfo) -> dict[str, str]:
        """
        Извлекает весь необходимый контекст для компиляции указанной функции.
        Возвращает словарь: {имя_файла: содержимое}.
        """
        from collections import defaultdict
        logger.debug(f"Извлечение контекста для функции {func.name}")
        result: dict[str, list[str]] = defaultdict(list)

        # Добавляем саму функцию
        result[func.location.name].append(func.source_text)

        # Добавляем функции, которые вызываются внутри этой
        called_functions = [f for f in self.functions if f.name in func.called_funcs]
        for called in called_functions:
            result[called.location.name].append(called.source_text)

        # Добавляем глобальные переменные, используемые внутри функции
        used_globals = [v for v in self.variables if v.name in func.external_variables]
        for var in used_globals:
            result[var.location.name].append(var.declaration)

        # Добавляем define'ы, используемые в теле функции
        all_defines = self.all_user_defined + self.all_system_defined
        for define in all_defines:
            if define.name in func.source_text:
                result[define.location.name].append(str(define))

        # Добавляем пользовательские типы, используемые в теле функции
        for t in self.types:
            if t.name and t.name in func.source_text:
                result[t.location.name].append(t.source_text)

        # Оставляем только непустые файлы
        filtered = {
            filename: "\n\n".join(parts)
            for filename, parts in result.items()
            if parts
        }

        return filtered

    @property
    def typedefs(self) -> List[TypedefInfo]:
        return [t for t in self.types if isinstance(t, TypedefInfo)]

    @property
    def enums(self) -> List[EnumInfo]:
        return [t for t in self.types if isinstance(t, EnumInfo)]

    @property
    def structs(self) -> List[StructInfo]:
        return [t for t in self.types if isinstance(t, StructInfo)]

    @property
    def unions(self) -> List[UnionInfo]:
        return [t for t in self.types if isinstance(t, UnionInfo)]

    @property
    def global_variables(self) -> list[VariableInfo]:
        seen = set()
        result = []
        for f in self.files:
            for gd in f.global_data:
                if gd.scope == "global" and gd not in seen:
                    seen.add(gd)
                    result.append(gd)
        return result

    @property
    def static_variables(self) -> list[VariableInfo]:
        seen = set()
        result = []
        for f in self.files:
            for gd in f.global_data:
                if gd.scope == "static" and gd not in seen:
                    seen.add(gd)
                    result.append(gd)
        return result

    @property
    def extern_variables(self) -> list[VariableInfo]:
        seen = set()
        result = []
        for f in self.files:
            for gd in f.global_data:
                if gd.scope == "extern" and gd not in seen:
                    seen.add(gd)
                    result.append(gd)
        return result

    @property
    def global_functions(self) -> list[FunctionInfo]:
        seen = set()
        result = []
        for f in self.files:
            for func in f.functions:
                if not func.is_static and func not in seen:
                    seen.add(func)
                    result.append(func)
        return result

    @property
    def static_functions(self) -> list[FunctionInfo]:
        seen = set()
        result = []
        for f in self.files:
            for func in f.functions:
                if func.is_static and func not in seen:
                    seen.add(func)
                    result.append(func)
        return result

    @property
    def all_types(self) -> list[BaseTypeInfo]:
        seen = set()
        result = []
        for f in self.files:
            for t in f.types:
                if t not in seen:
                    seen.add(t)
                    result.append(t)
        return result

    @property
    def all_user_defined(self) -> list[DefineInfo]:
        seen = set()
        result = []
        for f in self.files:
            for d in f.defines:
                if not d.is_system and d not in seen:
                    seen.add(d)
                    result.append(d)
        return result

    @property
    def all_system_defined(self) -> list[DefineInfo]:
        seen = set()
        result = []
        for f in self.files:
            for d in f.defines:
                if d.is_system and d not in seen:
                    seen.add(d)
                    result.append(d)
        return result

    @property
    def total_lines_with_comments(self) -> int:
        ret = 0
        for f in self.files:
            ret += f.total_lines_with_comments
        return ret

    @property
    def total_lines_without_comments(self) -> int:
        ret = 0
        for f in self.files:
            ret += f.lines_without_comments
        return ret

    @property
    def lines_pure_code(self) -> int:
        ret = 0
        for f in self.files:
            for func in f.functions:
                ret += func.lines_pure_code
        return ret

    @property
    def all_errors(self) -> list[DiagnosticInfo]:
        seen = set()
        result = []
        for f in self.files:
            for d in f.errors:
                if d not in seen:
                    seen.add(d)
                    result.append(d)

        # Сортировка по уровню severity (по возрастанию)
        result.sort(key=lambda d: d.severity, reverse=True)
        return result

    def __str__(self) -> str:
        lines = [
            f"Project at: {self.root_path}",
            f"Total files: {len(self.files)}",
            "Files:"
        ]
        for f in self.files:
            lines.append(f"  - {f.path.name} ({f.file_type})")
        return "\n".join(lines)