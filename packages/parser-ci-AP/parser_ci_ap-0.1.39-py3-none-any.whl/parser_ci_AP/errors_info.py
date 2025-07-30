from clang.cindex import Diagnostic

from .logger import logger

class DiagnosticInfo:
    def __init__(self, diag: Diagnostic):
        self.severity = diag.severity  # 1=warning, 2=error, 3=fatal, ...
        self.spelling = diag.spelling
        self.location = f"{diag.location.file}:{diag.location.line}"
        self.category = diag.category_name
        self.option = diag.option

        logger.debug(f"Clang diagnostic: [{self.severity}] {self.location}: {self.spelling}")

    @staticmethod
    def get_picklable_copy(obj: "DiagnosticInfo"):
        pass

    def __eq__(self, other):
        if not isinstance(other, DiagnosticInfo):
            return False
        return (
            self.severity == other.severity and
            self.spelling == other.spelling and
            self.location == other.location and
            self.category == other.category and
            self.option == other.option
        )

    def __hash__(self):
        return hash((
            self.severity,
            self.spelling,
            self.location,
            self.category,
            self.option
        ))

    def __str__(self):
        return f"[{self.severity}] {self.location}: {self.spelling}"