from enum import Enum


class FlowModuleValue2Type0AssetFallbackAccessTypesItemAccessType(str, Enum):
    R = "r"
    RW = "rw"
    W = "w"

    def __str__(self) -> str:
        return str(self.value)
