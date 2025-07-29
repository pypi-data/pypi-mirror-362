from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Histogram")


@_attrs_define
class Histogram:
    """
    Attributes:
        hist (list[float]):
        bin_edges (list[float]):
    """

    hist: list[float]
    bin_edges: list[float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hist = self.hist

        bin_edges = self.bin_edges

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "hist": hist,
                "bin_edges": bin_edges,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        hist = cast(list[float], d.pop("hist"))

        bin_edges = cast(list[float], d.pop("bin_edges"))

        histogram = cls(
            hist=hist,
            bin_edges=bin_edges,
        )

        histogram.additional_properties = d
        return histogram

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
