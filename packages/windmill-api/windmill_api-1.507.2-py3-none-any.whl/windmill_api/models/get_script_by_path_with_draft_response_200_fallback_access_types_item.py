from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_script_by_path_with_draft_response_200_fallback_access_types_item_access_type import (
    GetScriptByPathWithDraftResponse200FallbackAccessTypesItemAccessType,
)
from ..models.get_script_by_path_with_draft_response_200_fallback_access_types_item_kind import (
    GetScriptByPathWithDraftResponse200FallbackAccessTypesItemKind,
)

T = TypeVar("T", bound="GetScriptByPathWithDraftResponse200FallbackAccessTypesItem")


@_attrs_define
class GetScriptByPathWithDraftResponse200FallbackAccessTypesItem:
    """
    Attributes:
        path (str):
        kind (GetScriptByPathWithDraftResponse200FallbackAccessTypesItemKind):
        access_type (GetScriptByPathWithDraftResponse200FallbackAccessTypesItemAccessType):
    """

    path: str
    kind: GetScriptByPathWithDraftResponse200FallbackAccessTypesItemKind
    access_type: GetScriptByPathWithDraftResponse200FallbackAccessTypesItemAccessType
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

        kind = GetScriptByPathWithDraftResponse200FallbackAccessTypesItemKind(d.pop("kind"))

        access_type = GetScriptByPathWithDraftResponse200FallbackAccessTypesItemAccessType(d.pop("access_type"))

        get_script_by_path_with_draft_response_200_fallback_access_types_item = cls(
            path=path,
            kind=kind,
            access_type=access_type,
        )

        get_script_by_path_with_draft_response_200_fallback_access_types_item.additional_properties = d
        return get_script_by_path_with_draft_response_200_fallback_access_types_item

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
