from typing import Optional
from clang.cindex import Cursor, CursorKind
from pathlib import Path

from .logger import logger

class VariableInfo:
    def __init__(self, cursor: Cursor, encoding: str):
        self._cursor = cursor
        self.name = cursor.spelling
        self.location = Path(cursor.location.file.name).resolve() if cursor.location.file else Path()
        try:
            self._usr: str = cursor.get_usr()
        except (AttributeError, TypeError, UnicodeDecodeError):
            self._usr = f"{self.name}@{self.location}"
        self.encoding = encoding

        logger.debug(f"Создание VariableInfo для переменной: {self.name}")

        self.type: str
        self.scope: str
        self.size: Optional[int]
        self.declaration: str
        self.comment: str
        self.initial_value: str
        self.source_text: str

        self.type = cursor.type.spelling
        self.scope = self._get_scope(cursor)
        self.size = self._compute_size(cursor)
        self.declaration = self._extract_declaration()
        self.comment = self._extract_comments()
        self.initial_value = self._extract_initial_value()
        self.source_text = self._extract_source_text()

    @staticmethod
    def get_picklable_copy(obj: "VariableInfo"):
        obj._cursor = None
        obj._usr = None

    def _extract_initial_value(self) -> str:
        """
        Извлекает начальное значение переменной из текста объявления.
        Например: int x = 42; вернёт '42'
                  int arr[] = {1, 2}; вернёт '{1, 2}'
        """
        try:
            decl = self._extract_declaration()
            if '=' in decl:
                right = decl.split('=', 1)[1].rstrip(';').strip()
                return right
            return ""
        except Exception as e:
            logger.warning(f"{self.name}: ошибка при извлечении значения: {e}")
            return f"[!] Ошибка при извлечении значения переменной {self.name}: {e}"

    def _extract_comments(self) -> str:
        """
        Извлекает комментарии перед переменной:
        - однострочные (//, ///)
        - многострочные (/* ... */)
        - комментарии в одну строку: /* ... */
        Прекращает поиск при встрече пустой строки (если не внутри /**/).
        """
        try:
            if not self.location or not self.location.exists():
                return ""

            with open(self.location, "r", encoding=self.encoding, errors="replace") as f:
                lines = f.readlines()

            start_line = self._cursor.extent.start.line
            comments = []
            inside_block = False

            for i in range(start_line - 2, -1, -1):
                line = lines[i].rstrip("\n").rstrip("\r")
                stripped = line.strip()

                if not stripped and not inside_block:
                    break  # пустая строка завершает блок комментариев

                # Если вся строка — многострочный комментарий вида /* ... */
                if "/*" in stripped and "*/" in stripped:
                    comments.insert(0, line)
                    continue

                # Конец многострочного комментария
                if "*/" in stripped:
                    inside_block = True
                    comments.insert(0, line)
                    continue

                # Начало многострочного комментария
                if "/*" in stripped:
                    comments.insert(0, line)
                    inside_block = False
                    continue

                if inside_block:
                    comments.insert(0, line)
                    continue

                # Однострочные комментарии
                if stripped.startswith("//") or stripped.startswith("///"):
                    comments.insert(0, line)
                    continue

                break  # если не комментарий и не в блоке — остановка

            return "\n".join(comments).strip()

        except Exception as e:
            logger.warning(f"{self.name}: ошибка при извлечении комментариев: {e}")
            return f"[!] Ошибка при извлечении комментариев переменной {self.name}: {e}"

    def _extract_declaration(self) -> str:
        """
        Извлекает текст объявления переменной из файла (от начала до точки с запятой).
        """
        extent = self._cursor.extent
        start, end = extent.start, extent.end
        try:
            # Считываем все строки файла
            with open(start.file.name, "r", encoding=self.encoding, errors="replace") as f:
                lines = f.readlines()
            # Вырезаем диапазон строк объявления
            decl_lines = lines[start.line - 1:end.line]
            # Корректируем первую и последнюю строки по столбцам
            decl_lines[0] = decl_lines[0][start.column - 1:]
            decl_lines[-1] = decl_lines[-1][:end.column - 1]
            return "".join(decl_lines).strip()
        except Exception as e:
            logger.warning(f"{self.name}: ошибка извлечения объявления: {e}")
            return f"[!] Ошибка извлечения объявления переменной {self.name}: {e}"

    def _compute_size(self, cursor: Cursor) -> Optional[int]:
        """
        Вычисляет размер переменной в байтах.
        Возвращает None, если размер определить невозможно (например, для неполного типа).
        """
        try:
            sz = cursor.type.get_size()
            # clang возвращает -1, если не может определить размер
            return sz if sz != -1 else None
        except Exception as e:
            logger.warning(f"{self.name}: не удалось определить размер: {e}")
            return None

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

    def _get_scope(self, cursor: Cursor) -> str:
        """
        Определяет область видимости переменной: static, extern, local или global.
        """
        sc = cursor.storage_class.name
        if sc == "STATIC":
            return "static"
        elif sc == "EXTERN":
            return "extern"
        elif cursor.semantic_parent.kind.name == "FUNCTION_DECL":
            return "local"
        return "global"

    def describe(self) -> str:
        """
        Возвращает подробное описание переменной:
        - имя, тип, расположение
        - область видимости, размер, начальное значение
        - комментарий (если есть)
        - объявление
        """
        file = self.location.name if self.location else "<unknown>"
        line = self._cursor.extent.start.line

        out = [f"Variable: {self.name} ({file}:{line})"]
        out.append(f"  Type: {self.type}")
        out.append(f"  Scope: {self.scope}")
        if self.size is not None:
            out.append(f"  Size: {self.size} байт")
        if self.initial_value:
            out.append(f"  Initial value: {self.initial_value}")

        if self.comment:
            out.append("  Comment:")
            out.extend(f"    {line}" for line in self.comment.splitlines())

        out.append("  Declaration:")
        out.append("  -------------------------")
        out.extend(f"    {line}" for line in self.declaration.splitlines())

        return "\n".join(out)

    def __str__(self) -> str:
        return self.describe()

    def __eq__(self, other):
        if not isinstance(other, VariableInfo):
            return False
        return self._usr == other._usr

    def __hash__(self):
        return hash(self._usr)