import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.abstract_data_contract_api_version import AbstractDataContractApiVersion
from ..models.abstract_data_contract_kind import AbstractDataContractKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_server import ApiServer
    from ..models.custom_server import CustomServer
    from ..models.description import Description
    from ..models.price import Price
    from ..models.s3_server import S3Server


T = TypeVar("T", bound="AbstractDataContract")


@_attrs_define
class AbstractDataContract:
    """
    Attributes:
        id (Union[Unset, str]): A unique identifier used to reduce the risk of dataset name collisions, such as a UUID.
            This is an ODCS property and only has meaning for the data owner and is not used to identify data contracts in
            the Datavillage DCP
        version (Union[Unset, str]): Current version of the data contract.
        name (Union[Unset, str]): Name of the data contract.
        status (Union[Unset, str]): Current status of the dataset. Valid values are `production`, `test`, or
            `development`. Example: ['production', 'test', 'development'].
        api_version (Union[Unset, AbstractDataContractApiVersion]): Version of the standard used to build data contract.
            Default value is v3.0.0. Default: AbstractDataContractApiVersion.V3_0_0.
        kind (Union[Unset, AbstractDataContractKind]):  Default: AbstractDataContractKind.DATACONTRACT.
        tenant (Union[Unset, str]): Indicates the property the data is primarily associated with. Value is case
            insensitive.
        tags (Union[Unset, list[str]]): A list of tags that may be assigned to the elements (object or property); the
            tags keyword may appear at any level.
        data_product (Union[Unset, str]): The name of the data product.
        description (Union[Unset, Description]):
        price (Union[Unset, Price]):
        domain (Union[Unset, str]): Name of the logical data domain Example: ['imdb_ds_aggregate',
            'receiver_profile_out', 'transaction_profile_out'].
        sla_default_element (Union[Unset, str]): Element (using the element path notation) to do the checks on.
        contract_created_ts (Union[Unset, datetime.datetime]): Timestamp in UTC of when the data contract was created.
        servers (Union[Unset, list[Union['ApiServer', 'CustomServer', 'S3Server']]]): List of servers where the datasets
            reside.
    """

    id: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    api_version: Union[Unset, AbstractDataContractApiVersion] = AbstractDataContractApiVersion.V3_0_0
    kind: Union[Unset, AbstractDataContractKind] = AbstractDataContractKind.DATACONTRACT
    tenant: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    data_product: Union[Unset, str] = UNSET
    description: Union[Unset, "Description"] = UNSET
    price: Union[Unset, "Price"] = UNSET
    domain: Union[Unset, str] = UNSET
    sla_default_element: Union[Unset, str] = UNSET
    contract_created_ts: Union[Unset, datetime.datetime] = UNSET
    servers: Union[Unset, list[Union["ApiServer", "CustomServer", "S3Server"]]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_server import ApiServer
        from ..models.custom_server import CustomServer

        id = self.id

        version = self.version

        name = self.name

        status = self.status

        api_version: Union[Unset, str] = UNSET
        if not isinstance(self.api_version, Unset):
            api_version = self.api_version.value

        kind: Union[Unset, str] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        tenant = self.tenant

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        data_product = self.data_product

        description: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.description, Unset):
            description = self.description.to_dict()

        price: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        domain = self.domain

        sla_default_element = self.sla_default_element

        contract_created_ts: Union[Unset, str] = UNSET
        if not isinstance(self.contract_created_ts, Unset):
            contract_created_ts = self.contract_created_ts.isoformat()

        servers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.servers, Unset):
            servers = []
            for servers_item_data in self.servers:
                servers_item: dict[str, Any]
                if isinstance(servers_item_data, ApiServer):
                    servers_item = servers_item_data.to_dict()
                elif isinstance(servers_item_data, CustomServer):
                    servers_item = servers_item_data.to_dict()
                else:
                    servers_item = servers_item_data.to_dict()

                servers.append(servers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if version is not UNSET:
            field_dict["version"] = version
        if name is not UNSET:
            field_dict["name"] = name
        if status is not UNSET:
            field_dict["status"] = status
        if api_version is not UNSET:
            field_dict["apiVersion"] = api_version
        if kind is not UNSET:
            field_dict["kind"] = kind
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if tags is not UNSET:
            field_dict["tags"] = tags
        if data_product is not UNSET:
            field_dict["dataProduct"] = data_product
        if description is not UNSET:
            field_dict["description"] = description
        if price is not UNSET:
            field_dict["price"] = price
        if domain is not UNSET:
            field_dict["domain"] = domain
        if sla_default_element is not UNSET:
            field_dict["slaDefaultElement"] = sla_default_element
        if contract_created_ts is not UNSET:
            field_dict["contractCreatedTs"] = contract_created_ts
        if servers is not UNSET:
            field_dict["servers"] = servers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_server import ApiServer
        from ..models.custom_server import CustomServer
        from ..models.description import Description
        from ..models.price import Price
        from ..models.s3_server import S3Server

        d = dict(src_dict)
        id = d.pop("id", UNSET)

        version = d.pop("version", UNSET)

        name = d.pop("name", UNSET)

        status = d.pop("status", UNSET)

        _api_version = d.pop("apiVersion", UNSET)
        api_version: Union[Unset, AbstractDataContractApiVersion]
        if isinstance(_api_version, Unset):
            api_version = UNSET
        else:
            api_version = AbstractDataContractApiVersion(_api_version)

        _kind = d.pop("kind", UNSET)
        kind: Union[Unset, AbstractDataContractKind]
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = AbstractDataContractKind(_kind)

        tenant = d.pop("tenant", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        data_product = d.pop("dataProduct", UNSET)

        _description = d.pop("description", UNSET)
        description: Union[Unset, Description]
        if isinstance(_description, Unset):
            description = UNSET
        else:
            description = Description.from_dict(_description)

        _price = d.pop("price", UNSET)
        price: Union[Unset, Price]
        if isinstance(_price, Unset):
            price = UNSET
        else:
            price = Price.from_dict(_price)

        domain = d.pop("domain", UNSET)

        sla_default_element = d.pop("slaDefaultElement", UNSET)

        _contract_created_ts = d.pop("contractCreatedTs", UNSET)
        contract_created_ts: Union[Unset, datetime.datetime]
        if isinstance(_contract_created_ts, Unset):
            contract_created_ts = UNSET
        else:
            contract_created_ts = isoparse(_contract_created_ts)

        servers = []
        _servers = d.pop("servers", UNSET)
        for servers_item_data in _servers or []:

            def _parse_servers_item(data: object) -> Union["ApiServer", "CustomServer", "S3Server"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_odcs_server_type_0 = ApiServer.from_dict(data)

                    return componentsschemas_odcs_server_type_0
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_odcs_server_type_1 = CustomServer.from_dict(data)

                    return componentsschemas_odcs_server_type_1
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_odcs_server_type_2 = S3Server.from_dict(data)

                return componentsschemas_odcs_server_type_2

            servers_item = _parse_servers_item(servers_item_data)

            servers.append(servers_item)

        abstract_data_contract = cls(
            id=id,
            version=version,
            name=name,
            status=status,
            api_version=api_version,
            kind=kind,
            tenant=tenant,
            tags=tags,
            data_product=data_product,
            description=description,
            price=price,
            domain=domain,
            sla_default_element=sla_default_element,
            contract_created_ts=contract_created_ts,
            servers=servers,
        )

        abstract_data_contract.additional_properties = d
        return abstract_data_contract

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
