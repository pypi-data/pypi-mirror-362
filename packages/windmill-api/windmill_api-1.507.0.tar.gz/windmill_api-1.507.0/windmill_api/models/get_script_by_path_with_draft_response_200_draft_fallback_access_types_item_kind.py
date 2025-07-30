from enum import Enum


class GetScriptByPathWithDraftResponse200DraftFallbackAccessTypesItemKind(str, Enum):
    RESOURCE = "resource"
    S3OBJECT = "s3object"

    def __str__(self) -> str:
        return str(self.value)
