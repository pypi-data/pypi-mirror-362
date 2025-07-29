from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_script_json_body_fallback_access_types_item_access_type import (
    CreateScriptJsonBodyFallbackAccessTypesItemAccessType,
)
from ..models.create_script_json_body_fallback_access_types_item_kind import (
    CreateScriptJsonBodyFallbackAccessTypesItemKind,
)

T = TypeVar("T", bound="CreateScriptJsonBodyFallbackAccessTypesItem")


@_attrs_define
class CreateScriptJsonBodyFallbackAccessTypesItem:
    """
    Attributes:
        path (str):
        kind (CreateScriptJsonBodyFallbackAccessTypesItemKind):
        access_type (CreateScriptJsonBodyFallbackAccessTypesItemAccessType):
    """

    path: str
    kind: CreateScriptJsonBodyFallbackAccessTypesItemKind
    access_type: CreateScriptJsonBodyFallbackAccessTypesItemAccessType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind.value

        access_type = self.access_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
                "access_type": access_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        kind = CreateScriptJsonBodyFallbackAccessTypesItemKind(d.pop("kind"))

        access_type = CreateScriptJsonBodyFallbackAccessTypesItemAccessType(d.pop("access_type"))

        create_script_json_body_fallback_access_types_item = cls(
            path=path,
            kind=kind,
            access_type=access_type,
        )

        create_script_json_body_fallback_access_types_item.additional_properties = d
        return create_script_json_body_fallback_access_types_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
