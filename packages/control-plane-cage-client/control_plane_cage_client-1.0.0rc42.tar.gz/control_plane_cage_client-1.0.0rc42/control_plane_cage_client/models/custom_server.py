from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomServer")


@_attrs_define
class CustomServer:
    """Customise how data is fetched

    Attributes:
        type_ (str): Type of the server. Example: custom.
        location (Union[Unset, str]): A URL to a location.
        path (Union[Unset, str]): Relative or absolute path to the data file(s).
        account (Union[Unset, str]): Account used by the server.
        catalog (Union[Unset, str]): Name of the catalog.
        database (Union[Unset, str]): Name of the database.
        dataset (Union[Unset, str]): Name of the dataset.
        delimiter (Union[Unset, str]): Delimiter.
        endpoint_url (Union[Unset, str]): Server endpoint.
        format_ (Union[Unset, str]): File format.
        host (Union[Unset, str]): Host name or IP address.
        port (Union[Unset, int]): Port to the server. No default value is assumed for custom servers.
        project (Union[Unset, str]): Project name.
        region (Union[Unset, str]): Cloud region.
        region_name (Union[Unset, str]): Region name.
        schema (Union[Unset, str]): Name of the schema.
        service_name (Union[Unset, str]): Name of the service.
        staging_dir (Union[Unset, str]): Staging directory.
        warehouse (Union[Unset, str]): Name of the cluster or warehouse.
    """

    type_: str
    location: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    account: Union[Unset, str] = UNSET
    catalog: Union[Unset, str] = UNSET
    database: Union[Unset, str] = UNSET
    dataset: Union[Unset, str] = UNSET
    delimiter: Union[Unset, str] = UNSET
    endpoint_url: Union[Unset, str] = UNSET
    format_: Union[Unset, str] = UNSET
    host: Union[Unset, str] = UNSET
    port: Union[Unset, int] = UNSET
    project: Union[Unset, str] = UNSET
    region: Union[Unset, str] = UNSET
    region_name: Union[Unset, str] = UNSET
    schema: Union[Unset, str] = UNSET
    service_name: Union[Unset, str] = UNSET
    staging_dir: Union[Unset, str] = UNSET
    warehouse: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        location = self.location

        path = self.path

        account = self.account

        catalog = self.catalog

        database = self.database

        dataset = self.dataset

        delimiter = self.delimiter

        endpoint_url = self.endpoint_url

        format_ = self.format_

        host = self.host

        port = self.port

        project = self.project

        region = self.region

        region_name = self.region_name

        schema = self.schema

        service_name = self.service_name

        staging_dir = self.staging_dir

        warehouse = self.warehouse

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
            }
        )
        if location is not UNSET:
            field_dict["location"] = location
        if path is not UNSET:
            field_dict["path"] = path
        if account is not UNSET:
            field_dict["account"] = account
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if database is not UNSET:
            field_dict["database"] = database
        if dataset is not UNSET:
            field_dict["dataset"] = dataset
        if delimiter is not UNSET:
            field_dict["delimiter"] = delimiter
        if endpoint_url is not UNSET:
            field_dict["endpointUrl"] = endpoint_url
        if format_ is not UNSET:
            field_dict["format"] = format_
        if host is not UNSET:
            field_dict["host"] = host
        if port is not UNSET:
            field_dict["port"] = port
        if project is not UNSET:
            field_dict["project"] = project
        if region is not UNSET:
            field_dict["region"] = region
        if region_name is not UNSET:
            field_dict["regionName"] = region_name
        if schema is not UNSET:
            field_dict["schema"] = schema
        if service_name is not UNSET:
            field_dict["serviceName"] = service_name
        if staging_dir is not UNSET:
            field_dict["stagingDir"] = staging_dir
        if warehouse is not UNSET:
            field_dict["warehouse"] = warehouse

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = d.pop("type")

        location = d.pop("location", UNSET)

        path = d.pop("path", UNSET)

        account = d.pop("account", UNSET)

        catalog = d.pop("catalog", UNSET)

        database = d.pop("database", UNSET)

        dataset = d.pop("dataset", UNSET)

        delimiter = d.pop("delimiter", UNSET)

        endpoint_url = d.pop("endpointUrl", UNSET)

        format_ = d.pop("format", UNSET)

        host = d.pop("host", UNSET)

        port = d.pop("port", UNSET)

        project = d.pop("project", UNSET)

        region = d.pop("region", UNSET)

        region_name = d.pop("regionName", UNSET)

        schema = d.pop("schema", UNSET)

        service_name = d.pop("serviceName", UNSET)

        staging_dir = d.pop("stagingDir", UNSET)

        warehouse = d.pop("warehouse", UNSET)

        custom_server = cls(
            type_=type_,
            location=location,
            path=path,
            account=account,
            catalog=catalog,
            database=database,
            dataset=dataset,
            delimiter=delimiter,
            endpoint_url=endpoint_url,
            format_=format_,
            host=host,
            port=port,
            project=project,
            region=region,
            region_name=region_name,
            schema=schema,
            service_name=service_name,
            staging_dir=staging_dir,
            warehouse=warehouse,
        )

        custom_server.additional_properties = d
        return custom_server

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
