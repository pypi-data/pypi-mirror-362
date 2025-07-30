from enum import Enum


class CodeProviderRole(str, Enum):
    CODEPROVIDER = "CodeProvider"

    def __str__(self) -> str:
        return str(self.value)
