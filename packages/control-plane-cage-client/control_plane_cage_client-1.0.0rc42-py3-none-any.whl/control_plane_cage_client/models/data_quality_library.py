from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.data_quality_library_type import DataQualityLibraryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.any_type_type_5 import AnyTypeType5


T = TypeVar("T", bound="DataQualityLibrary")


@_attrs_define
class DataQualityLibrary:
    """
    Attributes:
        rule (str): Define a data quality check based on the predefined rules as per ODCS.
        type_ (Union[Unset, DataQualityLibraryType]): The type of quality check. 'text' is human-readable text that
            describes the quality of the data. 'library' is a set of maintained predefined quality attributes such as row
            count or unique. 'sql' is an individual SQL query that returns a value that can be compared. 'custom' is quality
            attributes that are vendor-specific, such as Soda or Great Expectations. Default:
            DataQualityLibraryType.LIBRARY.
        must_be (Union['AnyTypeType5', None, Unset, bool, float, int, list[Any], str]):
        must_not_be (Union['AnyTypeType5', None, Unset, bool, float, int, list[Any], str]):
        must_be_greater_than (Union[Unset, float]): Must be greater than the value to be valid. It is equivalent to '>'.
        must_be_greater_or_equal_to (Union[Unset, float]): Must be greater than or equal to the value to be valid. It is
            equivalent to '>='.
        must_be_less_than (Union[Unset, float]): Must be less than the value to be valid. It is equivalent to '<'.
        must_be_less_or_equal_to (Union[Unset, float]): Must be less than or equal to the value to be valid. It is
            equivalent to '<='.
        must_be_between (Union[None, Unset, list[float]]): Must be between the two numbers to be valid. Smallest number
            first in the array.
        must_not_be_between (Union[None, Unset, list[float]]): Must not be between the two numbers to be valid. Smallest
            number first in the array.
    """

    rule: str
    type_: Union[Unset, DataQualityLibraryType] = DataQualityLibraryType.LIBRARY
    must_be: Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str] = UNSET
    must_not_be: Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str] = UNSET
    must_be_greater_than: Union[Unset, float] = UNSET
    must_be_greater_or_equal_to: Union[Unset, float] = UNSET
    must_be_less_than: Union[Unset, float] = UNSET
    must_be_less_or_equal_to: Union[Unset, float] = UNSET
    must_be_between: Union[None, Unset, list[float]] = UNSET
    must_not_be_between: Union[None, Unset, list[float]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.any_type_type_5 import AnyTypeType5

        rule = self.rule

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        must_be: Union[None, Unset, bool, dict[str, Any], float, int, list[Any], str]
        if isinstance(self.must_be, Unset):
            must_be = UNSET
        elif isinstance(self.must_be, list):
            must_be = self.must_be

        elif isinstance(self.must_be, AnyTypeType5):
            must_be = self.must_be.to_dict()
        else:
            must_be = self.must_be

        must_not_be: Union[None, Unset, bool, dict[str, Any], float, int, list[Any], str]
        if isinstance(self.must_not_be, Unset):
            must_not_be = UNSET
        elif isinstance(self.must_not_be, list):
            must_not_be = self.must_not_be

        elif isinstance(self.must_not_be, AnyTypeType5):
            must_not_be = self.must_not_be.to_dict()
        else:
            must_not_be = self.must_not_be

        must_be_greater_than = self.must_be_greater_than

        must_be_greater_or_equal_to = self.must_be_greater_or_equal_to

        must_be_less_than = self.must_be_less_than

        must_be_less_or_equal_to = self.must_be_less_or_equal_to

        must_be_between: Union[None, Unset, list[float]]
        if isinstance(self.must_be_between, Unset):
            must_be_between = UNSET
        elif isinstance(self.must_be_between, list):
            must_be_between = self.must_be_between

        else:
            must_be_between = self.must_be_between

        must_not_be_between: Union[None, Unset, list[float]]
        if isinstance(self.must_not_be_between, Unset):
            must_not_be_between = UNSET
        elif isinstance(self.must_not_be_between, list):
            must_not_be_between = self.must_not_be_between

        else:
            must_not_be_between = self.must_not_be_between

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rule": rule,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if must_be is not UNSET:
            field_dict["mustBe"] = must_be
        if must_not_be is not UNSET:
            field_dict["mustNotBe"] = must_not_be
        if must_be_greater_than is not UNSET:
            field_dict["mustBeGreaterThan"] = must_be_greater_than
        if must_be_greater_or_equal_to is not UNSET:
            field_dict["mustBeGreaterOrEqualTo"] = must_be_greater_or_equal_to
        if must_be_less_than is not UNSET:
            field_dict["mustBeLessThan"] = must_be_less_than
        if must_be_less_or_equal_to is not UNSET:
            field_dict["mustBeLessOrEqualTo"] = must_be_less_or_equal_to
        if must_be_between is not UNSET:
            field_dict["mustBeBetween"] = must_be_between
        if must_not_be_between is not UNSET:
            field_dict["mustNotBeBetween"] = must_not_be_between

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.any_type_type_5 import AnyTypeType5

        d = dict(src_dict)
        rule = d.pop("rule")

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, DataQualityLibraryType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = DataQualityLibraryType(_type_)

        def _parse_must_be(data: object) -> Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_any_type_type_4 = cast(list[Any], data)

                return componentsschemas_any_type_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_any_type_type_5 = AnyTypeType5.from_dict(data)

                return componentsschemas_any_type_type_5
            except:  # noqa: E722
                pass
            return cast(Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str], data)

        must_be = _parse_must_be(d.pop("mustBe", UNSET))

        def _parse_must_not_be(data: object) -> Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                componentsschemas_any_type_type_4 = cast(list[Any], data)

                return componentsschemas_any_type_type_4
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_any_type_type_5 = AnyTypeType5.from_dict(data)

                return componentsschemas_any_type_type_5
            except:  # noqa: E722
                pass
            return cast(Union["AnyTypeType5", None, Unset, bool, float, int, list[Any], str], data)

        must_not_be = _parse_must_not_be(d.pop("mustNotBe", UNSET))

        must_be_greater_than = d.pop("mustBeGreaterThan", UNSET)

        must_be_greater_or_equal_to = d.pop("mustBeGreaterOrEqualTo", UNSET)

        must_be_less_than = d.pop("mustBeLessThan", UNSET)

        must_be_less_or_equal_to = d.pop("mustBeLessOrEqualTo", UNSET)

        def _parse_must_be_between(data: object) -> Union[None, Unset, list[float]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                must_be_between_type_0 = cast(list[float], data)

                return must_be_between_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[float]], data)

        must_be_between = _parse_must_be_between(d.pop("mustBeBetween", UNSET))

        def _parse_must_not_be_between(data: object) -> Union[None, Unset, list[float]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                must_not_be_between_type_0 = cast(list[float], data)

                return must_not_be_between_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[float]], data)

        must_not_be_between = _parse_must_not_be_between(d.pop("mustNotBeBetween", UNSET))

        data_quality_library = cls(
            rule=rule,
            type_=type_,
            must_be=must_be,
            must_not_be=must_not_be,
            must_be_greater_than=must_be_greater_than,
            must_be_greater_or_equal_to=must_be_greater_or_equal_to,
            must_be_less_than=must_be_less_than,
            must_be_less_or_equal_to=must_be_less_or_equal_to,
            must_be_between=must_be_between,
            must_not_be_between=must_not_be_between,
        )

        data_quality_library.additional_properties = d
        return data_quality_library

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
