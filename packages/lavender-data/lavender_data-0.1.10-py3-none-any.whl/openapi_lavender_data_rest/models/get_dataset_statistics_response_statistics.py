from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.categorical_column_statistics import CategoricalColumnStatistics
    from ..models.numeric_column_statistics import NumericColumnStatistics


T = TypeVar("T", bound="GetDatasetStatisticsResponseStatistics")


@_attrs_define
class GetDatasetStatisticsResponseStatistics:
    """ """

    additional_properties: dict[str, Union["CategoricalColumnStatistics", "NumericColumnStatistics"]] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        from ..models.numeric_column_statistics import NumericColumnStatistics

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, NumericColumnStatistics):
                field_dict[prop_name] = prop.to_dict()
            else:
                field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.categorical_column_statistics import CategoricalColumnStatistics
        from ..models.numeric_column_statistics import NumericColumnStatistics

        d = dict(src_dict)
        get_dataset_statistics_response_statistics = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union["CategoricalColumnStatistics", "NumericColumnStatistics"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_0 = NumericColumnStatistics.from_dict(data)

                    return additional_property_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                additional_property_type_1 = CategoricalColumnStatistics.from_dict(data)

                return additional_property_type_1

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        get_dataset_statistics_response_statistics.additional_properties = additional_properties
        return get_dataset_statistics_response_statistics

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union["CategoricalColumnStatistics", "NumericColumnStatistics"]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union["CategoricalColumnStatistics", "NumericColumnStatistics"]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
