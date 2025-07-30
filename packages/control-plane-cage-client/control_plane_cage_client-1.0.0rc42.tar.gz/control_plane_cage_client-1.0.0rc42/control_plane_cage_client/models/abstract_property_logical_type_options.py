import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AbstractPropertyLogicalTypeOptions")


@_attrs_define
class AbstractPropertyLogicalTypeOptions:
    """Metadata based on logicalType. This property needs to be set in order to set logicalTypeOptions.

    Attributes:
        minimum (Union[Unset, datetime.datetime, int]): logicalType = integer or logicalType = date. The minimum value.
        maximum (Union[Unset, datetime.datetime, int]): logicalType = integer or logicalType = date. The maximum value.
        pattern (Union[Unset, str]): logicalType = string. Regular expression pattern to define valid value. Follows
            regular expression syntax from ECMA-262 (https://262.ecma-international.org/5.1/#sec-15.10.1).
        exclusive_maximum (Union[Unset, bool]): logicalType = integer or logicalType = date. If set to true, all values
            are strictly less than the maximum value (values < maximum). Otherwise, less than or equal to the maximum value
            (values <= maximum).
        exclusive_minimum (Union[Unset, bool]): logicalType = integer or logicalType = date. If set to true, all values
            are strictly greater than the minimum value (values > minimum). Otherwise, greater than or equal to the minimum
            value (values >= minimum).
        multiple_of (Union[Unset, int]): logicalType = integer. Values must be multiples of this number. For example,
            multiple of 5 has valid values 0, 5, 10, -5.
        max_length (Union[Unset, int]): logicalType = string. Maximum length of the string.
        min_length (Union[Unset, int]): logicalType = string. Minimum length of the string.
        format_ (Union[Unset, str]): logicalType = date. How the date should be formatted using DuckDB notation. By
            default, the dates are formatted according to the ISO 8601 standard.
    """

    minimum: Union[Unset, datetime.datetime, int] = UNSET
    maximum: Union[Unset, datetime.datetime, int] = UNSET
    pattern: Union[Unset, str] = UNSET
    exclusive_maximum: Union[Unset, bool] = UNSET
    exclusive_minimum: Union[Unset, bool] = UNSET
    multiple_of: Union[Unset, int] = UNSET
    max_length: Union[Unset, int] = UNSET
    min_length: Union[Unset, int] = UNSET
    format_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        minimum: Union[Unset, int, str]
        if isinstance(self.minimum, Unset):
            minimum = UNSET
        elif isinstance(self.minimum, datetime.datetime):
            minimum = self.minimum.isoformat()
        else:
            minimum = self.minimum

        maximum: Union[Unset, int, str]
        if isinstance(self.maximum, Unset):
            maximum = UNSET
        elif isinstance(self.maximum, datetime.datetime):
            maximum = self.maximum.isoformat()
        else:
            maximum = self.maximum

        pattern = self.pattern

        exclusive_maximum = self.exclusive_maximum

        exclusive_minimum = self.exclusive_minimum

        multiple_of = self.multiple_of

        max_length = self.max_length

        min_length = self.min_length

        format_ = self.format_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if minimum is not UNSET:
            field_dict["minimum"] = minimum
        if maximum is not UNSET:
            field_dict["maximum"] = maximum
        if pattern is not UNSET:
            field_dict["pattern"] = pattern
        if exclusive_maximum is not UNSET:
            field_dict["exclusiveMaximum"] = exclusive_maximum
        if exclusive_minimum is not UNSET:
            field_dict["exclusiveMinimum"] = exclusive_minimum
        if multiple_of is not UNSET:
            field_dict["multipleOf"] = multiple_of
        if max_length is not UNSET:
            field_dict["maxLength"] = max_length
        if min_length is not UNSET:
            field_dict["minLength"] = min_length
        if format_ is not UNSET:
            field_dict["format"] = format_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_minimum(data: object) -> Union[Unset, datetime.datetime, int]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                minimum_type_0 = isoparse(data)

                return minimum_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, int], data)

        minimum = _parse_minimum(d.pop("minimum", UNSET))

        def _parse_maximum(data: object) -> Union[Unset, datetime.datetime, int]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                maximum_type_0 = isoparse(data)

                return maximum_type_0
            except:  # noqa: E722
                pass
            return cast(Union[Unset, datetime.datetime, int], data)

        maximum = _parse_maximum(d.pop("maximum", UNSET))

        pattern = d.pop("pattern", UNSET)

        exclusive_maximum = d.pop("exclusiveMaximum", UNSET)

        exclusive_minimum = d.pop("exclusiveMinimum", UNSET)

        multiple_of = d.pop("multipleOf", UNSET)

        max_length = d.pop("maxLength", UNSET)

        min_length = d.pop("minLength", UNSET)

        format_ = d.pop("format", UNSET)

        abstract_property_logical_type_options = cls(
            minimum=minimum,
            maximum=maximum,
            pattern=pattern,
            exclusive_maximum=exclusive_maximum,
            exclusive_minimum=exclusive_minimum,
            multiple_of=multiple_of,
            max_length=max_length,
            min_length=min_length,
            format_=format_,
        )

        abstract_property_logical_type_options.additional_properties = d
        return abstract_property_logical_type_options

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
