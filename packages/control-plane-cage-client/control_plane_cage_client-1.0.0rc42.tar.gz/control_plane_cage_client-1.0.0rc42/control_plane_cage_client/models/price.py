from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Price")


@_attrs_define
class Price:
    """
    Attributes:
        price_amount (Union[Unset, float]): Subscription price per unit of measure in `priceUnit`.
        price_currency (Union[Unset, str]): Currency of the subscription price in `priceAmount`.
        price_unit (Union[Unset, str]): The unit of measure for calculating cost. Examples megabyte, gigabyte.
    """

    price_amount: Union[Unset, float] = UNSET
    price_currency: Union[Unset, str] = UNSET
    price_unit: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        price_amount = self.price_amount

        price_currency = self.price_currency

        price_unit = self.price_unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if price_amount is not UNSET:
            field_dict["priceAmount"] = price_amount
        if price_currency is not UNSET:
            field_dict["priceCurrency"] = price_currency
        if price_unit is not UNSET:
            field_dict["priceUnit"] = price_unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        price_amount = d.pop("priceAmount", UNSET)

        price_currency = d.pop("priceCurrency", UNSET)

        price_unit = d.pop("priceUnit", UNSET)

        price = cls(
            price_amount=price_amount,
            price_currency=price_currency,
            price_unit=price_unit,
        )

        price.additional_properties = d
        return price

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
