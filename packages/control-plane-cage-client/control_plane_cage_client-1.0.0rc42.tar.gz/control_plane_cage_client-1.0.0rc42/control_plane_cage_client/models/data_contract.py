import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.data_contract_odcs import DataContractODCS


T = TypeVar("T", bound="DataContract")


@_attrs_define
class DataContract:
    """ODCS compliant description of a data contract with metadata fields added by Datavillage DCP

    Attributes:
        id (str): A unique identifier used in the Datavillage DCP to identify a data contract
        client_id (str): Id of the client owning the data contract
        created (datetime.datetime): The date and time when the document was created.
        updated (datetime.datetime): The date and time of the last update to the document.
        data_contract (DataContractODCS):
    """

    id: str
    client_id: str
    created: datetime.datetime
    updated: datetime.datetime
    data_contract: "DataContractODCS"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        client_id = self.client_id

        created = self.created.isoformat()

        updated = self.updated.isoformat()

        data_contract = self.data_contract.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "clientId": client_id,
                "created": created,
                "updated": updated,
                "dataContract": data_contract,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_contract_odcs import DataContractODCS

        d = dict(src_dict)
        id = d.pop("id")

        client_id = d.pop("clientId")

        created = isoparse(d.pop("created"))

        updated = isoparse(d.pop("updated"))

        data_contract = DataContractODCS.from_dict(d.pop("dataContract"))

        data_contract = cls(
            id=id,
            client_id=client_id,
            created=created,
            updated=updated,
            data_contract=data_contract,
        )

        data_contract.additional_properties = d
        return data_contract

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
