from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_script_with_draft_draft_fallback_access_types_item_access_type import (
    NewScriptWithDraftDraftFallbackAccessTypesItemAccessType,
)
from ..models.new_script_with_draft_draft_fallback_access_types_item_kind import (
    NewScriptWithDraftDraftFallbackAccessTypesItemKind,
)

T = TypeVar("T", bound="NewScriptWithDraftDraftFallbackAccessTypesItem")


@_attrs_define
class NewScriptWithDraftDraftFallbackAccessTypesItem:
    """
    Attributes:
        path (str):
        kind (NewScriptWithDraftDraftFallbackAccessTypesItemKind):
        access_type (NewScriptWithDraftDraftFallbackAccessTypesItemAccessType):
    """

    path: str
    kind: NewScriptWithDraftDraftFallbackAccessTypesItemKind
    access_type: NewScriptWithDraftDraftFallbackAccessTypesItemAccessType
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

        kind = NewScriptWithDraftDraftFallbackAccessTypesItemKind(d.pop("kind"))

        access_type = NewScriptWithDraftDraftFallbackAccessTypesItemAccessType(d.pop("access_type"))

        new_script_with_draft_draft_fallback_access_types_item = cls(
            path=path,
            kind=kind,
            access_type=access_type,
        )

        new_script_with_draft_draft_fallback_access_types_item.additional_properties = d
        return new_script_with_draft_draft_fallback_access_types_item

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
