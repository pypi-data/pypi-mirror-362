from typing import Optional, List
from pathlib import Path
from clang.cindex import Cursor
import re

from .logger import logger

class DefineInfo:
    def __init__(self, cursor: Cursor, encoding: str):
        self._cursor = cursor
        self.name: str = cursor.spelling
        self.location: Path = (
            Path(cursor.location.file.name).resolve()
            if cursor.location.file
            else Path()
        )
        try:
            self._usr: str = cursor.get_usr()
        except (AttributeError, TypeError, UnicodeDecodeError):
            self._usr = f"{self.name}@{self.location}"
        self.encoding = encoding

        logger.debug(f"Создание DefineInfo: {self.name}")

        self._raw_line: str
        self.params: Optional[List[str]]
        self.value: str
        self.comment: str
        self.is_system: bool
        self.source_text: str

        self._raw_line = self._read_raw_line()
        self.params = self._extract_params()
        self.value = self._extract_value()
        self.comment = self._extract_comment_after()
        self.is_system = self._detect_system_define()  # Дефайны которые не используются кодом напрямую
        self.source_text = self._raw_line

    @staticmethod
    def get_picklable_copy(obj: "DefineInfo"):
        obj._cursor = None
        obj._usr = None

    def _detect_system_define(self) -> bool:
        """
        Определяет, является ли define системным:
        - начинается с '_'
        - или у него отсутствует значение (value)
        """
        return self.name.startswith("_") or not self.value

    def _read_raw_line(self) -> str:
        """
        Считывает строку исходника, содержащую #define.
        """
        try:
            line_num = self._cursor.location.line
            with open(self.location, "r", encoding=self.encoding, errors="replace") as f:
                lines = f.readlines()
                return lines[line_num - 1].strip()
        except Exception as e:
            #logger.warning(f"{self.name}: ошибка чтения строки #define: {e}")
            return f"[!] Ошибка чтения строки define {self.name}: {e}"

    def _extract_params(self) -> Optional[list]:
        """
        Извлекает параметры только если после имени макроса СРАЗУ идёт '(' (без пробела!).
        Если параметров нет — возвращает None.
        """
        pattern = rf'^#\s*define\s+{re.escape(self.name)}\(([^)]*)\)'
        match = re.match(pattern, self._raw_line)
        if match:
            params = [p.strip() for p in match.group(1).split(",") if p.strip()]
            return params
        return None

    def _extract_value(self) -> str:
        """
        Извлекает значение define.
        Для макроса с параметрами: всё после закрывающей скобки параметров.
        Для макроса без параметров: всё после имени макроса.
        """
        # С параметрами — ищем после скобки
        pattern = rf'^#\s*define\s+{re.escape(self.name)}\([^\)]*\)\s*(.*)'
        match = re.match(pattern, self._raw_line)
        if match:
            value_part = match.group(1)
        else:
            # Без параметров — всё, что после имени (в т.ч. если пробел перед '(')
            pattern = rf'^#\s*define\s+{re.escape(self.name)}\s+(.*)'
            match = re.match(pattern, self._raw_line)
            value_part = match.group(1) if match else ""
        # убираем комментарии
        for comment in ['//', '/*']:
            if comment in value_part:
                value_part = value_part.split(comment, 1)[0].strip()
        return value_part.strip()

    def _extract_comment_after(self) -> str:
        """
        Извлекает комментарий после значения define (если он есть).
        """
        try:
            for marker in ["//", "/*"]:
                if marker in self._raw_line:
                    return self._raw_line.split(marker, 1)[1].strip()
            return ""
        except Exception as e:
            logger.warning(f"{self.name}: ошибка извлечения комментария: {e}")
            return ""

    def describe(self) -> str:
        loc_str = f"{self.location}:{self._cursor.location.line}"
        system_flag = "[system] " if self.is_system else ""
        params_str = f"({', '.join(self.params)})" if self.params else ""
        value_str = f" {self.value}" if self.value else ""
        comment_str = f" // {self.comment}" if self.comment else ""
        return f"{system_flag}#define {self.name}{params_str}{value_str}{comment_str}  // from {loc_str}"

    def __str__(self) -> str:
        return self.describe()

    def __eq__(self, other):
        if not isinstance(other, DefineInfo):
            return False
        return self._usr == other._usr

    def __hash__(self):
        return hash(self._usr)
