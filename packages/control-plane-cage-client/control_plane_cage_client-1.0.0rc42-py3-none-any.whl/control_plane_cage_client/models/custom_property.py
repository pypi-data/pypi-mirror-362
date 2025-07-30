from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.any_type_type_5 import AnyTypeType5


T = TypeVar("T", bound="CustomProperty")


@_attrs_define
class CustomProperty:
    """
    Attributes:
        property_ (Union[Unset, str]): The name of the key. Names should be in camel-case the same as if they were
            permanent properties in the contract.
        value (Union['AnyTypeType5', None, Unset, bool, float, int, list[Any], str]):
    """

    property_: Union[Unset, str] = UNSET
    value: Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.any_type_type_5 import AnyTypeType5

        property_ = self.property_

        value: Union[None, Unset, bool, dict[str, Any], float, int, list[Any], str]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, list):
            value = self.value

        elif isinstance(self.value, AnyTypeType5):
            value = self.value.to_dict()
        else:
            value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if property_ is not UNSET:
            field_dict["property"] = property_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.any_type_type_5 import AnyTypeType5

        d = dict(src_dict)
        property_ = d.pop("property", UNSET)

        def _parse_value(data: object) -> Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_any_type_type_4 = cast(list[Any], data)

                return componentsschemas_any_type_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_any_type_type_5 = AnyTypeType5.from_dict(data)

                return componentsschemas_any_type_type_5
            except:  # noqa: E722
                pass
            return cast(Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str], data)

        value = _parse_value(d.pop("value", UNSET))

        custom_property = cls(
            property_=property_,
            value=value,
        )

        custom_property.additional_properties = d
        return custom_property

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
