from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AlgoSource")


@_attrs_define
class AlgoSource:
    """
    Attributes:
        registry (str):
        image (str):
        tag (str):
        secret (Union[Unset, str]): A value that will be interpreted as an ImagePullSecret. An example would be a github
            access token that has at least the scope `packages:read`, base64 encoded as `username:token`. If no value is
            provided no ImagePullSecret will be used when deploying the cage.
    """

    registry: str
    image: str
    tag: str
    secret: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        registry = self.registry

        image = self.image

        tag = self.tag

        secret = self.secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "registry": registry,
                "image": image,
                "tag": tag,
            }
        )
        if secret is not UNSET:
            field_dict["secret"] = secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        registry = d.pop("registry")

        image = d.pop("image")

        tag = d.pop("tag")

        secret = d.pop("secret", UNSET)

        algo_source = cls(
            registry=registry,
            image=image,
            tag=tag,
            secret=secret,
        )

        algo_source.additional_properties = d
        return algo_source

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
