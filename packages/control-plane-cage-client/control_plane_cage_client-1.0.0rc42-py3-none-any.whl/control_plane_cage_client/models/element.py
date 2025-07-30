from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.data_quality_library import DataQualityLibrary
    from ..models.data_quality_sql import DataQualitySql


T = TypeVar("T", bound="Element")


@_attrs_define
class Element:
    """
    Attributes:
        physical_type (Union[Unset, str]): The physical element data type in the data source. Example: ['table', 'view',
            'topic', 'file'].
        description (Union[Unset, str]): Description of the element.
        business_name (Union[Unset, str]): The business name of the element.
        tags (Union[Unset, list[str]]): A list of tags that may be assigned to the elements (object or property); the
            tags keyword may appear at any level.
        quality (Union[Unset, list[Union['DataQualityLibrary', 'DataQualitySql']]]): Data quality rules with all the
            relevant information for rule setup and execution
    """

    physical_type: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    business_name: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    quality: Union[Unset, list[Union["DataQualityLibrary", "DataQualitySql"]]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.data_quality_library import DataQualityLibrary

        physical_type = self.physical_type

        description = self.description

        business_name = self.business_name

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        quality: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.quality, Unset):
            quality = []
            for componentsschemas_data_quality_item_data in self.quality:
                componentsschemas_data_quality_item: dict[str, Any]
                if isinstance(componentsschemas_data_quality_item_data, DataQualityLibrary):
                    componentsschemas_data_quality_item = componentsschemas_data_quality_item_data.to_dict()
                else:
                    componentsschemas_data_quality_item = componentsschemas_data_quality_item_data.to_dict()

                quality.append(componentsschemas_data_quality_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if physical_type is not UNSET:
            field_dict["physicalType"] = physical_type
        if description is not UNSET:
            field_dict["description"] = description
        if business_name is not UNSET:
            field_dict["businessName"] = business_name
        if tags is not UNSET:
            field_dict["tags"] = tags
        if quality is not UNSET:
            field_dict["quality"] = quality

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.data_quality_library import DataQualityLibrary
        from ..models.data_quality_sql import DataQualitySql

        d = dict(src_dict)
        physical_type = d.pop("physicalType", UNSET)

        description = d.pop("description", UNSET)

        business_name = d.pop("businessName", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        quality = []
        _quality = d.pop("quality", UNSET)
        for componentsschemas_data_quality_item_data in _quality or []:

            def _parse_componentsschemas_data_quality_item(
                data: object,
            ) -> Union["DataQualityLibrary", "DataQualitySql"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    componentsschemas_data_quality_item_type_0 = DataQualityLibrary.from_dict(data)

                    return componentsschemas_data_quality_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_data_quality_item_type_1 = DataQualitySql.from_dict(data)

                return componentsschemas_data_quality_item_type_1

            componentsschemas_data_quality_item = _parse_componentsschemas_data_quality_item(
                componentsschemas_data_quality_item_data
            )

            quality.append(componentsschemas_data_quality_item)

        element = cls(
            physical_type=physical_type,
            description=description,
            business_name=business_name,
            tags=tags,
            quality=quality,
        )

        element.additional_properties = d
        return element

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
