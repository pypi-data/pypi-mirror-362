from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.code_provider_role import CodeProviderRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.algo_source import AlgoSource
    from ..models.code_provider_settings import CodeProviderSettings
    from ..models.cron import Cron


T = TypeVar("T", bound="CodeProvider")


@_attrs_define
class CodeProvider:
    """Someone who provides code

    Attributes:
        role (Union[Unset, CodeProviderRole]):  Example: CodeProvider.
        settings (Union[Unset, CodeProviderSettings]):
        cron (Union[Unset, list['Cron']]):
        source (Union[Unset, AlgoSource]):
    """

    role: Union[Unset, CodeProviderRole] = UNSET
    settings: Union[Unset, "CodeProviderSettings"] = UNSET
    cron: Union[Unset, list["Cron"]] = UNSET
    source: Union[Unset, "AlgoSource"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        cron: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cron, Unset):
            cron = []
            for cron_item_data in self.cron:
                cron_item = cron_item_data.to_dict()
                cron.append(cron_item)

        source: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if role is not UNSET:
            field_dict["role"] = role
        if settings is not UNSET:
            field_dict["settings"] = settings
        if cron is not UNSET:
            field_dict["cron"] = cron
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.algo_source import AlgoSource
        from ..models.code_provider_settings import CodeProviderSettings
        from ..models.cron import Cron

        d = dict(src_dict)
        _role = d.pop("role", UNSET)
        role: Union[Unset, CodeProviderRole]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = CodeProviderRole(_role)

        _settings = d.pop("settings", UNSET)
        settings: Union[Unset, CodeProviderSettings]
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = CodeProviderSettings.from_dict(_settings)

        cron = []
        _cron = d.pop("cron", UNSET)
        for cron_item_data in _cron or []:
            cron_item = Cron.from_dict(cron_item_data)

            cron.append(cron_item)

        _source = d.pop("source", UNSET)
        source: Union[Unset, AlgoSource]
        if isinstance(_source, Unset):
            source = UNSET
        else:
            source = AlgoSource.from_dict(_source)

        code_provider = cls(
            role=role,
            settings=settings,
            cron=cron,
            source=source,
        )

        code_provider.additional_properties = d
        return code_provider

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
