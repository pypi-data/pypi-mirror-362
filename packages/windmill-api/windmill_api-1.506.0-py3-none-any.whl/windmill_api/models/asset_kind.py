from enum import Enum


class AssetKind(str, Enum):
    RESOURCE = "resource"
    S3OBJECT = "s3object"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return str(self.value)
