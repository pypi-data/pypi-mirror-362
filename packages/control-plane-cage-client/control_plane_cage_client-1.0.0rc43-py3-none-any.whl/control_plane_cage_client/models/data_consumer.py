from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_consumer_role import DataConsumerRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_server import ApiServer
    from ..models.custom_server import CustomServer
    from ..models.data_consumer_settings import DataConsumerSettings
    from ..models.s3_server import S3Server


T = TypeVar("T", bound="DataConsumer")


@_attrs_define
class DataConsumer:
    """Someone who consumes data

    Attributes:
        role (Union[Unset, DataConsumerRole]):  Example: DataConsumer.
        server (Union['ApiServer', 'CustomServer', 'S3Server', Unset]): Data source details of where data is physically
            stored.
        settings (Union[Unset, DataConsumerSettings]):
    """

    role: Union[Unset, DataConsumerRole] = UNSET
    server: Union["ApiServer", "CustomServer", "S3Server", Unset] = UNSET
    settings: Union[Unset, "DataConsumerSettings"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.api_server import ApiServer
        from ..models.custom_server import CustomServer

        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        server: Union[Unset, dict[str, Any]]
        if isinstance(self.server, Unset):
            server = UNSET
        elif isinstance(self.server, ApiServer):
            server = self.server.to_dict()
        elif isinstance(self.server, CustomServer):
            server = self.server.to_dict()
        else:
            server = self.server.to_dict()

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role is not UNSET:
            field_dict["role"] = role
        if server is not UNSET:
            field_dict["server"] = server
        if settings is not UNSET:
            field_dict["settings"] = settings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.api_server import ApiServer
        from ..models.custom_server import CustomServer
        from ..models.data_consumer_settings import DataConsumerSettings
        from ..models.s3_server import S3Server

        d = dict(src_dict)
        _role = d.pop("role", UNSET)
        role: Union[Unset, DataConsumerRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = DataConsumerRole(_role)

        def _parse_server(data: object) -> Union["ApiServer", "CustomServer", "S3Server", Unset]:
            if isinstance(data, Unset):
                return data
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

        server = _parse_server(d.pop("server", UNSET))

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, DataConsumerSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = DataConsumerSettings.from_dict(_settings)

        data_consumer = cls(
            role=role,
            server=server,
            settings=settings,
        )

        data_consumer.additional_properties = d
        return data_consumer

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
