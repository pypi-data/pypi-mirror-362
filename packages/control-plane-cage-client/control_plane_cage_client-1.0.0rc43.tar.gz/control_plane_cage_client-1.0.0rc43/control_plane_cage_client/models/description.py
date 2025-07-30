from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Description")


@_attrs_define
class Description:
    """
    Attributes:
        usage (Union[Unset, str]): Intended usage of the dataset.
        purpose (Union[Unset, str]): Purpose of the dataset.
        limitations (Union[Unset, str]): Limitations of the dataset.
    """

    usage: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    limitations: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        usage = self.usage

        purpose = self.purpose

        limitations = self.limitations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if usage is not UNSET:
            field_dict["usage"] = usage
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if limitations is not UNSET:
            field_dict["limitations"] = limitations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        usage = d.pop("usage", UNSET)

        purpose = d.pop("purpose", UNSET)

        limitations = d.pop("limitations", UNSET)

        description = cls(
            usage=usage,
            purpose=purpose,
            limitations=limitations,
        )

        description.additional_properties = d
        return description

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
