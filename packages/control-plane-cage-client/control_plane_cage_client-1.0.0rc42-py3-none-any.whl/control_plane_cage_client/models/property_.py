from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.abstract_property_logical_type import AbstractPropertyLogicalType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.abstract_property_logical_type_options import AbstractPropertyLogicalTypeOptions
    from ..models.any_type_type_5 import AnyTypeType5
    from ..models.data_quality_library import DataQualityLibrary
    from ..models.data_quality_sql import DataQualitySql


T = TypeVar("T", bound="Property")


@_attrs_define
class Property:
    """Identifiable ODCS description of a property

    Attributes:
        id (str):
        name (str):
        physical_type (Union[Unset, str]): The physical element data type in the data source. For example, VARCHAR(2),
            DOUBLE, INT. Example: ['table', 'view', 'topic', 'file'].
        description (Union[Unset, str]): Description of the element.
        business_name (Union[Unset, str]): The business name of the element.
        tags (Union[Unset, list[str]]): A list of tags that may be assigned to the elements (object or property); the
            tags keyword may appear at any level.
        quality (Union[Unset, list[Union['DataQualityLibrary', 'DataQualitySql']]]): Data quality rules with all the
            relevant information for rule setup and execution
        examples (Union[Unset, list[Union['AnyTypeType5', None, bool, float, int, list[Any], str]]]): List of sample
            element values.
        primary_key (Union[Unset, bool]): Boolean value specifying whether the element is primary or not. Default is
            false.
        primary_key_position (Union[Unset, int]): If element is a primary key, the position of the primary key element.
            Starts from 1. Example of `account_id, name` being primary key columns, `account_id` has primaryKeyPosition 1
            and `name` primaryKeyPosition 2. Default to -1.
        logical_type (Union[Unset, AbstractPropertyLogicalType]):
        logical_type_options (Union[Unset, AbstractPropertyLogicalTypeOptions]): Metadata based on logicalType. This
            property needs to be set in order to set logicalTypeOptions.
        required (Union[Unset, bool]): Indicates if the element may contain Null values; possible values are true and
            false. Default is false.
        unique (Union[Unset, bool]): Indicates if the element contains unique values; possible values are true and
            false. Default is false.
        partitioned (Union[Unset, bool]): Indicates if the element is partitioned; possible values are true and false.
        partition_key_position (Union[Unset, int]): If element is used for partitioning, the position of the partition
            element. Starts from 1. Example of `country, year` being partition columns, `country` has partitionKeyPosition 1
            and `year` partitionKeyPosition 2. Default to -1.
        classification (Union[Unset, str]): Can be anything, like confidential, restricted, and public to more advanced
            categorization. Some companies like PayPal, use data classification indicating the class of data in the element;
            expected values are 1, 2, 3, 4, or 5. Example: ['confidential', 'restricted', 'public'].
        encrypted_name (Union[Unset, str]): The element name within the dataset that contains the encrypted element
            value. For example, unencrypted element `email_address` might have an encryptedName of `email_address_encrypt`.
        transform_source_objects (Union[Unset, list[str]]): List of objects in the data source used in the
            transformation.
        transform_logic (Union[Unset, str]): Logic used in the element transformation.
        transform_description (Union[Unset, str]): Describes the transform logic in very simple terms.
        critical_data_element (Union[Unset, bool]): True or false indicator; If element is considered a critical data
            element (CDE) then true else false.
    """

    id: str
    name: str
    physical_type: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    business_name: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    quality: Union[Unset, list[Union["DataQualityLibrary", "DataQualitySql"]]] = UNSET
    examples: Union[Unset, list[Union["AnyTypeType5", None, bool, float, int, list[Any], str]]] = UNSET
    primary_key: Union[Unset, bool] = UNSET
    primary_key_position: Union[Unset, int] = UNSET
    logical_type: Union[Unset, AbstractPropertyLogicalType] = UNSET
    logical_type_options: Union[Unset, "AbstractPropertyLogicalTypeOptions"] = UNSET
    required: Union[Unset, bool] = UNSET
    unique: Union[Unset, bool] = UNSET
    partitioned: Union[Unset, bool] = UNSET
    partition_key_position: Union[Unset, int] = UNSET
    classification: Union[Unset, str] = UNSET
    encrypted_name: Union[Unset, str] = UNSET
    transform_source_objects: Union[Unset, list[str]] = UNSET
    transform_logic: Union[Unset, str] = UNSET
    transform_description: Union[Unset, str] = UNSET
    critical_data_element: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.any_type_type_5 import AnyTypeType5
        from ..models.data_quality_library import DataQualityLibrary

        id = self.id

        name = self.name

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

        examples: Union[Unset, list[Union[None, bool, dict[str, Any], float, int, list[Any], str]]] = UNSET
        if not isinstance(self.examples, Unset):
            examples = []
            for examples_item_data in self.examples:
                examples_item: Union[None, bool, dict[str, Any], float, int, list[Any], str]
                if isinstance(examples_item_data, list):
                    examples_item = examples_item_data

                elif isinstance(examples_item_data, AnyTypeType5):
                    examples_item = examples_item_data.to_dict()
                else:
                    examples_item = examples_item_data
                examples.append(examples_item)

        primary_key = self.primary_key

        primary_key_position = self.primary_key_position

        logical_type: Union[Unset, str] = UNSET
        if not isinstance(self.logical_type, Unset):
            logical_type = self.logical_type.value

        logical_type_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.logical_type_options, Unset):
            logical_type_options = self.logical_type_options.to_dict()

        required = self.required

        unique = self.unique

        partitioned = self.partitioned

        partition_key_position = self.partition_key_position

        classification = self.classification

        encrypted_name = self.encrypted_name

        transform_source_objects: Union[Unset, list[str]] = UNSET
        if not isinstance(self.transform_source_objects, Unset):
            transform_source_objects = self.transform_source_objects

        transform_logic = self.transform_logic

        transform_description = self.transform_description

        critical_data_element = self.critical_data_element

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
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
        if examples is not UNSET:
            field_dict["examples"] = examples
        if primary_key is not UNSET:
            field_dict["primaryKey"] = primary_key
        if primary_key_position is not UNSET:
            field_dict["primaryKeyPosition"] = primary_key_position
        if logical_type is not UNSET:
            field_dict["logicalType"] = logical_type
        if logical_type_options is not UNSET:
            field_dict["logicalTypeOptions"] = logical_type_options
        if required is not UNSET:
            field_dict["required"] = required
        if unique is not UNSET:
            field_dict["unique"] = unique
        if partitioned is not UNSET:
            field_dict["partitioned"] = partitioned
        if partition_key_position is not UNSET:
            field_dict["partitionKeyPosition"] = partition_key_position
        if classification is not UNSET:
            field_dict["classification"] = classification
        if encrypted_name is not UNSET:
            field_dict["encryptedName"] = encrypted_name
        if transform_source_objects is not UNSET:
            field_dict["transformSourceObjects"] = transform_source_objects
        if transform_logic is not UNSET:
            field_dict["transformLogic"] = transform_logic
        if transform_description is not UNSET:
            field_dict["transformDescription"] = transform_description
        if critical_data_element is not UNSET:
            field_dict["criticalDataElement"] = critical_data_element

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.abstract_property_logical_type_options import AbstractPropertyLogicalTypeOptions
        from ..models.any_type_type_5 import AnyTypeType5
        from ..models.data_quality_library import DataQualityLibrary
        from ..models.data_quality_sql import DataQualitySql

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

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

        examples = []
        _examples = d.pop("examples", UNSET)
        for examples_item_data in _examples or []:

            def _parse_examples_item(data: object) -> Union["AnyTypeType5", None, bool, float, int, list[Any], str]:
                if data is None:
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
                return cast(Union["AnyTypeType5", None, bool, float, int, list[Any], str], data)

            examples_item = _parse_examples_item(examples_item_data)

            examples.append(examples_item)

        primary_key = d.pop("primaryKey", UNSET)

        primary_key_position = d.pop("primaryKeyPosition", UNSET)

        _logical_type = d.pop("logicalType", UNSET)
        logical_type: Union[Unset, AbstractPropertyLogicalType]
        if isinstance(_logical_type, Unset):
            logical_type = UNSET
        else:
            logical_type = AbstractPropertyLogicalType(_logical_type)

        _logical_type_options = d.pop("logicalTypeOptions", UNSET)
        logical_type_options: Union[Unset, AbstractPropertyLogicalTypeOptions]
        if isinstance(_logical_type_options, Unset):
            logical_type_options = UNSET
        else:
            logical_type_options = AbstractPropertyLogicalTypeOptions.from_dict(_logical_type_options)

        required = d.pop("required", UNSET)

        unique = d.pop("unique", UNSET)

        partitioned = d.pop("partitioned", UNSET)

        partition_key_position = d.pop("partitionKeyPosition", UNSET)

        classification = d.pop("classification", UNSET)

        encrypted_name = d.pop("encryptedName", UNSET)

        transform_source_objects = cast(list[str], d.pop("transformSourceObjects", UNSET))

        transform_logic = d.pop("transformLogic", UNSET)

        transform_description = d.pop("transformDescription", UNSET)

        critical_data_element = d.pop("criticalDataElement", UNSET)

        property_ = cls(
            id=id,
            name=name,
            physical_type=physical_type,
            description=description,
            business_name=business_name,
            tags=tags,
            quality=quality,
            examples=examples,
            primary_key=primary_key,
            primary_key_position=primary_key_position,
            logical_type=logical_type,
            logical_type_options=logical_type_options,
            required=required,
            unique=unique,
            partitioned=partitioned,
            partition_key_position=partition_key_position,
            classification=classification,
            encrypted_name=encrypted_name,
            transform_source_objects=transform_source_objects,
            transform_logic=transform_logic,
            transform_description=transform_description,
            critical_data_element=critical_data_element,
        )

        property_.additional_properties = d
        return property_

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
