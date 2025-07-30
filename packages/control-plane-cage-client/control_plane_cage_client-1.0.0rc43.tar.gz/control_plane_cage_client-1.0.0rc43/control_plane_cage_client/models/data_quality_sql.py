from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_quality_sql_type import DataQualitySqlType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataQualitySql")


@_attrs_define
class DataQualitySql:
    """
    Attributes:
        query (str): Query string that adheres to the dialect of the provided server.
        type_ (Union[Unset, DataQualitySqlType]): The type of quality check. 'text' is human-readable text that
            describes the quality of the data. 'library' is a set of maintained predefined quality attributes such as row
            count or unique. 'sql' is an individual SQL query that returns a value that can be compared. 'custom' is quality
            attributes that are vendor-specific, such as Soda or Great Expectations. Default: DataQualitySqlType.LIBRARY.
    """

    query: str
    type_: Union[Unset, DataQualitySqlType] = DataQualitySqlType.LIBRARY
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        query = self.query

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "query": query,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        query = d.pop("query")

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, DataQualitySqlType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = DataQualitySqlType(_type_)

        data_quality_sql = cls(
            query=query,
            type_=type_,
        )

        data_quality_sql.additional_properties = d
        return data_quality_sql

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
