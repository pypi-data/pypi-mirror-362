from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AuthoritativeDefinition")


@_attrs_define
class AuthoritativeDefinition:
    """Link to source that provides more details on the dataset; examples would be a link to an external definition, a
    training video, a GitHub repo, Collibra, or another tool. Authoritative definitions follow the same structure in the
    standard.

        Attributes:
            url (str): URL to the authority.
            type_ (str): Type of definition for authority: v2.3 adds standard values: `businessDefinition`,
                `transformationImplementation`, `videoTutorial`, `tutorial`, and `implementation`.
    """

    url: str
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        type_ = d.pop("type")

        authoritative_definition = cls(
            url=url,
            type_=type_,
        )

        authoritative_definition.additional_properties = d
        return authoritative_definition

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
