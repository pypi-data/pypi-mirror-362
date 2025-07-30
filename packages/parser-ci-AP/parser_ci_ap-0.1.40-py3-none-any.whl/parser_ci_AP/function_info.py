from clang.cindex import Cursor, CursorKind, StorageClass
from pathlib import Path
import re
from typing import Set, Optional

from .logger import logger
from .variable_info import VariableInfo
from .define_info import DefineInfo

class FunctionInfo:
    def __init__(self, cursor: Cursor, encoding: str):
        self._cursor = cursor
        self.name = cursor.spelling
        self.location = Path(cursor.location.file.name).resolve() if cursor.location.file else Path()
        try:
            self._usr = cursor.get_usr()  # Уникальный идентификатор функции
        except Exception:
            self._usr = f"{self.name}@{self.location}"
        self.encoding = encoding

        logger.debug(f"Создание FunctionInfo для функции {self.name}")

        self.return_var: Optional[ReturnInfo] = None
        self.args: list[VariableInfo] = []
        self.source_text: str
        self.is_static: bool = False
        self.comment: str
        self.lines_functional: int
        self.local_variables: list[VariableInfo] = []
        self.called_funcs: Set[str] = set()
        self.lines_pure_code: int
        self.used_macros: Set[str] = set()

        self.source_text = self._extract_source_text()
        self.comment = self._extract_comments()
        self._count_functional_lines()
        self._extract_args()
        self.external_variables = set()
        self._extract_external_variables()
        self.return_var = self._extract_return_variable()
        self._detect_static()
        self._count_pure_code_lines()

        self._extract_from_cursor()

        set_loc_var = {obj.name for obj in self.local_variables}
        self.external_variables = self.external_variables - set_loc_var - self.called_funcs

    @staticmethod
    def get_picklable_copy(obj: "FunctionInfo"):
        obj._cursor = None
        for lv in obj.local_variables:
            lv.get_picklable_copy(lv)
        for ar in obj.args:
            ar.get_picklable_copy(ar)

    def _count_pure_code_lines(self):
        """
        Подсчитывает количество строк, содержащих только чистый код:
        - без комментариев (// и /* */)
        - без пустых строк
        """
        code = self.source_text

        # Удаляем многострочные комментарии
        code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

        # Удаляем однострочные комментарии
        code = re.sub(r"//.*", "", code)

        # Оставляем только строки с кодом
        self.lines_pure_code = sum(1 for line in code.splitlines() if line.strip())
        logger.debug(f"{self.name}: строк чистого кода = {self.lines_pure_code}")

    def _extract_return_variable(self) -> Optional["ReturnInfo"]:
        """
        Извлекает информацию о возвращаемом значении функции:
        - тип возврата
        - выражение после return (если есть)
        """
        logger.debug(f"{self.name}: извлечение return-выражения")
        return_type = self._cursor.result_type.spelling
        return_expr = None

        def visit(node: Cursor):
            nonlocal return_expr
            if node.kind.name == "RETURN_STMT":
                tokens = [t.spelling for t in node.get_tokens()]
                if len(tokens) > 1:
                    return_expr = " ".join(tokens[1:])  # Пропускаем 'return'
            for child in node.get_children():
                visit(child)

        visit(self._cursor)

        if return_expr is None:
            return None
        return ReturnInfo(return_type, return_expr)

    def _detect_static(self):
        """
        Определяет, является ли функция статической, используя только canonical-курсоры.
        """
        try:
            canonical = self._cursor.canonical
            if canonical and canonical.storage_class == StorageClass.STATIC:
                self.is_static = True
                logger.debug(f"{self.name}: является static")
        except Exception:
            logger.warning(f"{self.name}: не удалось определить static")

        return False

    def _extract_args(self):
        """
        Извлекает аргументы функции как объекты VariableInfo.
        """
        logger.debug(f"{self.name}: извлечение аргументов")
        self.args = []
        for arg in self._cursor.get_arguments():
            if arg.kind == CursorKind.PARM_DECL and arg.spelling:
                self.args.append(VariableInfo(arg, self.encoding))

    def _extract_source_text(self):
        extent = self._cursor.extent
        start = extent.start
        end = extent.end

        def extract_lines(lines):
            lines = lines[start.line - 1:end.line]
            lines[0] = lines[0][start.column - 1:]
            lines[-1] = lines[-1][:end.column - 1]
            return "".join(lines).strip()

        try:
            with open(self.location, "r", encoding=self.encoding, errors="replace") as f:
                return extract_lines(f.readlines())
        except Exception as e:
            logger.warning(f"{self.name}: ошибка извлечения текста функции: {e}")
            return f"[!] Ошибка извлечения текста функции {self.name}: {e}"

    def _extract_comments(self) -> str:
        """
        Пытается извлечь комментарии, расположенные перед началом функции.
        Поддерживает:
          - однострочные // и ///
          - многострочные /* ... */
        Останавливается при встрече пустой строки.
        """
        try:
            with open(self.location, "r", encoding=self.encoding, errors="replace") as f:
                lines = f.readlines()

            start_line = self._cursor.extent.start.line
            comments = []
            inside_block = False

            for i in range(start_line - 2, -1, -1):
                line = lines[i].rstrip()

                if not line.strip() and not inside_block:
                    break  # пустая строка прерывает комментарий

                # Обрабатываем многострочные комментарии (/* ... */)
                if "*/" in line:
                    inside_block = True
                    comments.insert(0, line)
                    continue

                if inside_block:
                    comments.insert(0, line)
                    if "/*" in line:
                        inside_block = False
                    continue

                # Однострочные комментарии
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("///"):
                    comments.insert(0, line)
                    continue

                break  # не комментарий и не внутри блока — прерываем

            return "\n".join(comments).strip()

        except Exception as e:
            logger.warning(f"{self.name}: ошибка извлечения комментариев: {e}")
            return f"[!] Ошибка при извлечении комментариев функции {self.name}: {e}"

    def _count_functional_lines(self):
        """
        Подсчитывает количество строк с функциональным кодом.
        Убирает комментарии `//`, `/* */` и пустые строки.
        """
        code = self.source_text

        # Удаляем многострочные комментарии (включая переносы строк)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

        # Удаляем однострочные комментарии
        code = re.sub(r'//.*', '', code)

        # Разбиваем на строки и фильтруем только те, что содержат код
        lines = code.splitlines()
        functional_lines = [line for line in lines if line.strip()]  # только непустые

        self.lines_functional = len(functional_lines)
        logger.debug(f"{self.name}: строк с функциональным кодом = {self.lines_functional}")

    def _extract_from_cursor(self):
        logger.debug(f"{self.name}: обход курсора для переменных и вызовов функций")
        def visit(node: Cursor):
            if node.kind == CursorKind.VAR_DECL:
                self.local_variables.append(VariableInfo(node, self.encoding))
            elif node.kind == CursorKind.CALL_EXPR:
                called_name = node.spelling or node.displayname or "<unnamed_call>"
                self.called_funcs.add(called_name)
            for child in node.get_children():
                visit(child)

        visit(self._cursor)

    def _extract_external_variables(self):
        """
        Находит все переменные, которые используются в функции, но не являются:
        - её аргументами
        - локальными переменными

        Это потенциально глобальные или внешние переменные.
        """
        logger.debug(f"{self.name}: извлечение внешних переменных")
        local_and_args = {var.name for var in self.local_variables}
        local_and_args.update(arg.name for arg in self.args)

        external_vars = set()

        def visit(node: Cursor):
            if node.kind == CursorKind.DECL_REF_EXPR:
                decl = node.referenced
                if not decl:
                    return
                if decl.kind == CursorKind.VAR_DECL:
                    name = decl.spelling
                    if name and name not in local_and_args:
                        external_vars.add(name)
            for child in node.get_children():
                visit(child)

        visit(self._cursor)
        self.external_variables = external_vars

    def extract_used_macros(self, defines: list["DefineInfo"]):
        """
        Находит все макросы (define), используемые в исходном тексте функции.
        В self.used_macros сохраняет не имена, а сами объекты DefineInfo.
        :param defines: список объектов DefineInfo (только не системные макросы)
        """
        used = set()
        for define in defines:
            macro = define.name
            if re.search(rf"\b{re.escape(macro)}\b", self.source_text):
                used.add(define)
        self.used_macros = used

    def describe(self):
        out = [f"Function: {self.name} ({self.location})"]
        out.append(f"  Return type: {self.return_var.describe() if self.return_var else 'void'}")
        out.append(f"  Static: {'yes' if self.is_static else 'no'}")
        out.append(f"  Functional lines: {self.lines_functional}")

        if self.local_variables:
            out.append("  Local variables:")
            for var in self.local_variables:
                out.append(f"    - {var.type} {var.name}")

        if self.args:
            out.append("  Arguments:")
            for arg in self.args:
                out.append(f"    - {arg.type} {arg.name}")

        if self.called_funcs:
            out.append("  Called functions:")
            for name in self.called_funcs:
                out.append(f"    - {name}")

        if self.external_variables:
            out.append("  External variables:")
            for name in self.external_variables:
                out.append(f"    - {name}")

        if self.used_macros:
            out.append("  Used macros:")
            for define in self.used_macros:
                out.append(f"    - {define.name}")

        return "\n".join(out)

    def __str__(self):
        return self.describe()

    def __eq__(self, other):
        if not isinstance(other, FunctionInfo):
            return False
        return self._usr == other._usr

    def __hash__(self):
        return hash(self._usr)

class ReturnInfo:
    def __init__(self, return_type: str, expression: Optional[str] = None):
        self.type = return_type
        self.expression = expression

    def describe(self) -> str:
        desc = f"Return type: {self.type}"
        if self.expression:
            desc += f", returns: {self.expression}"
        return desc

    def __str__(self):
        return self.describe()