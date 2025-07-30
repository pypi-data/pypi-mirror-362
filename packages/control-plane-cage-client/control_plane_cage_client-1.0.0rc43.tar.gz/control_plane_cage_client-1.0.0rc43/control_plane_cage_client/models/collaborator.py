from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.abstract_collaborator_configuration import AbstractCollaboratorConfiguration


T = TypeVar("T", bound="Collaborator")


@_attrs_define
class Collaborator:
    """Collaborator

    Attributes:
        id (str):
        client_id (str):
        name (Union[Unset, str]): A name given the collaborator. This value is intended to be read by humans. Example:
            My Collaborator.
        label (Union[Unset, str]): A label given the collaborator. This value is intended to refered to in code.
            Example: my-collaborator.
        role (Union[Unset, str]):
        configuration (Union[Unset, AbstractCollaboratorConfiguration]): A configuration of the collaborator. This is an
            object representing key-value pairs that will be available in the cage as environment variables.
    """

    id: str
    client_id: str
    name: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    role: Union[Unset, str] = UNSET
    configuration: Union[Unset, "AbstractCollaboratorConfiguration"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        client_id = self.client_id

        name = self.name

        label = self.label

        role = self.role

        configuration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.configuration, Unset):
            configuration = self.configuration.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "clientId": client_id,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if label is not UNSET:
            field_dict["label"] = label
        if role is not UNSET:
            field_dict["role"] = role
        if configuration is not UNSET:
            field_dict["configuration"] = configuration

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.abstract_collaborator_configuration import AbstractCollaboratorConfiguration

        d = dict(src_dict)
        id = d.pop("id")

        client_id = d.pop("clientId")

        name = d.pop("name", UNSET)

        label = d.pop("label", UNSET)

        role = d.pop("role", UNSET)

        _configuration = d.pop("configuration", UNSET)
        configuration: Union[Unset, AbstractCollaboratorConfiguration]
        if isinstance(_configuration, Unset):
            configuration = UNSET
        else:
            configuration = AbstractCollaboratorConfiguration.from_dict(_configuration)

        collaborator = cls(
            id=id,
            client_id=client_id,
            name=name,
            label=label,
            role=role,
            configuration=configuration,
        )

        collaborator.additional_properties = d
        return collaborator

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
