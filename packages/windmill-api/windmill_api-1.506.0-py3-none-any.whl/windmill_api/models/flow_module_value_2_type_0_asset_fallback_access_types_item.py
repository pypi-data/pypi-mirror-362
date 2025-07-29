from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.flow_module_value_2_type_0_asset_fallback_access_types_item_access_type import (
    FlowModuleValue2Type0AssetFallbackAccessTypesItemAccessType,
)
from ..models.flow_module_value_2_type_0_asset_fallback_access_types_item_kind import (
    FlowModuleValue2Type0AssetFallbackAccessTypesItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type0AssetFallbackAccessTypesItem")


@_attrs_define
class FlowModuleValue2Type0AssetFallbackAccessTypesItem:
    """
    Attributes:
        path (str):
        kind (FlowModuleValue2Type0AssetFallbackAccessTypesItemKind):
        access_type (Union[Unset, FlowModuleValue2Type0AssetFallbackAccessTypesItemAccessType]):
    """

    path: str
    kind: FlowModuleValue2Type0AssetFallbackAccessTypesItemKind
    access_type: Union[Unset, FlowModuleValue2Type0AssetFallbackAccessTypesItemAccessType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind.value

        access_type: Union[Unset, str] = UNSET
        if not isinstance(self.access_type, Unset):
            access_type = self.access_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
            }
        )
        if access_type is not UNSET:
            field_dict["access_type"] = access_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        kind = FlowModuleValue2Type0AssetFallbackAccessTypesItemKind(d.pop("kind"))

        _access_type = d.pop("access_type", UNSET)
        access_type: Union[Unset, FlowModuleValue2Type0AssetFallbackAccessTypesItemAccessType]
        if isinstance(_access_type, Unset):
            access_type = UNSET
        else:
            access_type = FlowModuleValue2Type0AssetFallbackAccessTypesItemAccessType(_access_type)

        flow_module_value_2_type_0_asset_fallback_access_types_item = cls(
            path=path,
            kind=kind,
            access_type=access_type,
        )

        flow_module_value_2_type_0_asset_fallback_access_types_item.additional_properties = d
        return flow_module_value_2_type_0_asset_fallback_access_types_item

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
