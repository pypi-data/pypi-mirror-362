from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Literal, Set, Optional
from clang import cindex
from clang.cindex import CursorKind
import re
import chardet
from clang.cindex import TranslationUnit as TU

from .logger import logger
from .type_info import BaseTypeInfo, StructInfo, UnionInfo, EnumInfo, TypedefInfo
from .function_info import FunctionInfo
from .variable_info import VariableInfo
from .define_info import DefineInfo
from .errors_info import DiagnosticInfo


class AbstractProjectFile(ABC):
    def __init__(self, path: Path, root_path: Path):
        self._tu: cindex.TranslationUnit
        self.path: Path = path
        self.root_path = root_path.resolve()

        self.total_lines_with_comments: int = 0       # Общее количество строк
        self.lines_without_comments: int = 0          # Строки без комментариев (включая директивы и пустые)
        self.lines_functional: int = 0                # Строки кода внутри функций (без комментариев)

        self.types: List[BaseTypeInfo] = []
        self.file_type: Literal["c", "h"] = "c"
        self.includes: List[str] = []
        self.all_includes: Set[Path] = set()
        self.encoding: str
        self.functions: List[FunctionInfo] = []
        self.global_data: List[VariableInfo] = []
        self.defines: List[DefineInfo] = []
        self.errors: List[DiagnosticInfo] = []

        self.encoding = self._detect_encoding()
        self.file_type = self._detect_file_type()
        self.source_text = self._extract_source_text()

    @staticmethod
    def get_picklable_copy(obj: "AbstractProjectFile"):
        obj._tu = None

        for t in obj.types:
            t.get_picklable_copy(t)

        for f in obj.functions:
            f.get_picklable_copy(f)

        for gb in obj.global_data:
            gb.get_picklable_copy(gb)

        for df in obj.defines:
            df.get_picklable_copy(df)

        for dg in obj.errors:
            dg.get_picklable_copy(dg)

    def _detect_encoding(self) -> str:
        """
        Определяет кодировку файла. Порядок попыток:
        1. windows-1251
        2. utf-8
        3. Автоопределение через chardet
        """
        # 1. windows-1251
        try:
            with open(self.path, "r", encoding="windows-1251") as f:
                f.read()
                logger.debug(f"{self.path}: windows-1251")
            return "windows-1251"
        except UnicodeDecodeError:
            pass

        # 2. utf-8
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                f.read()
                logger.debug(f"{self.path}: utf-8")
            return "utf-8"
        except UnicodeDecodeError:
            pass

        # 3. auto-detect
        try:
            with open(self.path, "rb") as f:
                raw = f.read()
                result = chardet.detect(raw)
                detected = result.get("encoding", "utf-8") or "utf-8"
                logger.debug(f"{self.path}: chardet detected {detected}")
                return detected
        except Exception as e:
            logger.warning(f"Не удалось определить кодировку файла {self.path}: {e}")
            return "utf-8"

    def _extract_source_text(self) -> str:
        """
        Читает исходный текст файла с сохранением кодировки.
        Возвращает весь текст как одну строку.
        В случае ошибки — логирует и возвращает пустую строку.
        """
        try:
            with open(self.path, "r", encoding=self.encoding) as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Не удалось прочитать файл {self.path} с кодировкой {self.encoding}: {e}")
            return ""

    def _detect_file_type(self) -> Literal["c", "h"]:
        ext = self.path.suffix.lower()
        return "h" if ext == ".h" else "c"

    @abstractmethod
    def analyze(self):
        """Анализирует файл и заполняет поля: строки, функции, типы и т.д."""
        pass

    @abstractmethod
    def collect_all_includes_recursively(self, set_in: Set[Path]):
        """Устанавливает множество всех файлов, включаемых в данный файл напрямую или косвенно (транзитивно)."""
        pass

    @abstractmethod
    def analyze_with_clang(self):
        pass

    @property
    @abstractmethod
    def all_user_defined(self) -> list[DefineInfo]:
        pass

    @property
    @abstractmethod
    def all_system_defined(self) -> list[DefineInfo]:
        pass

    @property
    @abstractmethod
    def all_global_data(self) -> list[VariableInfo]:
        pass

class ProjectFile(AbstractProjectFile):
    def __init__(self, path: Path, root_path: Path):
        logger.debug(f"Создание ProjectFile для {path}")
        super().__init__(path, root_path)
        self._tu: Optional[cindex.TranslationUnit] = None
        self.analyze()

    def collect_all_includes_recursively(self, set_in: Set[Path]):
        self.all_includes = set_in

    def analyze_with_clang(self):
        logger.debug(f"Анализ {self.path} с Clang")
        tu = self._parse_with_clang()
        self._tu = tu
        if tu:
            self._extract_from_ast(tu)
            self._extract_defines(tu)
            self._extract_diagnostics(tu)
        else:
            logger.warning(f"Clang не смог проанализировать {self.path}")

    def _extract_diagnostics(self, tu: cindex.TranslationUnit):
        self.errors = [DiagnosticInfo(diag) for diag in tu.diagnostics]

    def analyze(self):
        logger.info(f"Анализ строк и includes: {self.path}")
        self.total_lines_with_comments = self._count_lines_with_comments()
        self.lines_without_comments = self._count_lines_without_comments()
        self._extract_includes()

    def _count_lines_with_comments(self) -> int:
        """
        Считает количество строк в файле, исключая только пустые строки.
        Учитываются строки с кодом, комментариями, директивами препроцессора и т.п.
        """
        try:
            with open(self.path, "r", encoding=self.encoding, errors="replace") as f:
                return sum(1 for line in f if line.strip())
        except Exception as e:
            logger.warning(f"Ошибка при подсчёте строк с комментариями в {self.path}: {e}")
            return 0

    def _count_lines_without_comments(self) -> int:
        """
        Считает количество строк без комментариев и пустых строк.
        Удаляет как однострочные (//) так и многострочные (/* */) комментарии.
        """
        try:
            with open(self.path, "r", encoding=self.encoding, errors="replace") as f:
                code = f.read()

            # Удаляем многострочные комментарии (включая переносы строк)
            code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

            # Удаляем однострочные комментарии
            code = re.sub(r"//.*", "", code)

            # Оставляем только непустые строки
            return sum(1 for line in code.splitlines() if line.strip())

        except Exception as e:
            logger.warning(f"Ошибка при подсчёте строк без комментариев в {self.path}: {e}")
            return 0

    def _extract_includes(self):
        includes = []
        include_pattern = re.compile(r'^\s*#\s*include\s*[<"](.+?)[">]')
        with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = include_pattern.match(line)
                if match:
                    includes.append(match.group(1))
        self.includes = includes

    def _parse_with_clang(self) -> cindex.TranslationUnit | None:
        index = cindex.Index.create()

        # Строим include-пути ТОЛЬКО из all_includes
        include_dirs = {p.parent.resolve() for p in self.all_includes}
        include_dirs.add(self.path.parent.resolve())  # на всякий случай — папка самого файла

        args = [
            "-x", "c",
            "-std=c11",
            *[f"-I{str(p)}" for p in include_dirs],
            "-ferror-limit=1000000"  # Максимальное число ошибок при диагностики
        ]

        options = (
                TU.PARSE_DETAILED_PROCESSING_RECORD |
                TU.PARSE_INCLUDE_BRIEF_COMMENTS_IN_CODE_COMPLETION
        )

        try:
            return index.parse(str(self.path), args=args, options=options)
        except cindex.TranslationUnitLoadError as e:
            logger.warning(f"Ошибка при анализе {self.path}: {e}")
            return None

    def _extract_from_ast(self, tu: cindex.TranslationUnit):
        """
        Обходит AST-файл один раз и извлекает все нужные сущности:
        - типы (struct, union, enum, typedef)
        - функции
        - ...
        """
        logger.debug(f"Обход AST: {self.path}")
        def visit(cursor):

            # Типы
            if cursor.kind == CursorKind.STRUCT_DECL and cursor.spelling:
                self.types.append(StructInfo(cursor, self.encoding))
            elif cursor.kind == CursorKind.UNION_DECL and cursor.spelling:
                self.types.append(UnionInfo(cursor, self.encoding))
            elif cursor.kind == CursorKind.ENUM_DECL and cursor.spelling:
                self.types.append(EnumInfo(cursor, self.encoding))
            elif cursor.kind == CursorKind.TYPEDEF_DECL and cursor.spelling:
                target = cursor.underlying_typedef_type.get_declaration()
                if target.kind not in {
                    CursorKind.ENUM_DECL,
                    CursorKind.STRUCT_DECL,
                    CursorKind.UNION_DECL,
                }:
                    self.types.append(TypedefInfo(cursor, self.encoding))

            # Функции
            elif cursor.kind == CursorKind.FUNCTION_DECL:
                if cursor.is_definition():
                    if str(cursor.location.file) == str(self.path):
                        self.functions.append(FunctionInfo(cursor, self.encoding))

            elif cursor.kind == CursorKind.VAR_DECL:
                if cursor.semantic_parent == tu.cursor:
                    self.global_data.append(VariableInfo(cursor, self.encoding))

            # Рекурсивно вглубь
            for child in cursor.get_children():
                visit(child)

        visit(tu.cursor)

    def _extract_defines(self, tu: cindex.TranslationUnit):
        """
        Извлекает все #define-директивы из TranslationUnit и сохраняет их в self.defines.
        """
        logger.debug(f"Извлечение define-директив: {self.path}")
        self.defines.clear()
        def visit(cursor):
            if cursor.kind == CursorKind.MACRO_DEFINITION and cursor.spelling:
                try:
                    self.defines.append(DefineInfo(cursor, self.encoding))
                except Exception as e:
                    logger.warning(f"Не удалось обработать define '{cursor.spelling}': {e}")
            for child in cursor.get_children():
                visit(child)

        visit(tu.cursor)

    @property
    def all_user_defined(self) -> list[DefineInfo]:
        seen = set()
        result = []
        for d in self.defines:
            if not d.is_system and d not in seen:
                seen.add(d)
                result.append(d)
        return result

    @property
    def all_system_defined(self) -> list[DefineInfo]:
        seen = set()
        result = []
        for d in self.defines:
            if d.is_system and d not in seen:
                seen.add(d)
                result.append(d)
        return result

    @property
    def all_global_data(self) -> list[VariableInfo]:
        seen = set()
        result = []
        for gd in self.global_data:
            if gd.scope == "global" and gd not in seen:
                seen.add(gd)
                result.append(gd)
        return result

    def __str__(self) -> str:
        lines = [
            f"File: {self.path.name}",
            f"  Type: {self.file_type}",
            f"  Total lines: {self.total_lines_with_comments}",
            f"  Lines without comments: {self.lines_without_comments}",
            f"  Functional lines: {self.lines_functional}",
            f"  Functions: {len(self.functions)}",
            f"  Types: {len(self.types)}",
            f"  Includes: {', '.join(self.includes)}",
            f"  All includes: {', '.join(str(p) for p in self.all_includes)}",
            f"  Global variables: {len(self.global_data)}",
            f"  User macros: {len(self.all_user_defined)}",
            f"  System macros: {len(self.all_system_defined)}",
        ]

        if self.functions:
            lines.append("  Function list:")
            for f in self.functions:
                lines.append(f"    - {f.name}")

        if self.global_data:
            lines.append("  Global variables:")
            for v in self.global_data:
                lines.append(f"    - {v.type} {v.name}")

        if self.all_user_defined:
            lines.append("  User defines:")
            for d in self.all_user_defined:
                lines.append(f"    - {d.describe()}")

        if self.all_system_defined:
            lines.append("  System defines:")
            for d in self.all_system_defined:
                lines.append(f"    - {d.describe()}")

        if self.errors:
            lines.append("  Diagnostics:")
            for e in self.errors:
                lines.append(f"    - {str(e)}")

        return "\n".join(lines)
