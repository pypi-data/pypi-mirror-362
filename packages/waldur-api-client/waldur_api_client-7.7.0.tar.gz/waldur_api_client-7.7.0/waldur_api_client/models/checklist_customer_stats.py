from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ChecklistCustomerStats")


@_attrs_define
class ChecklistCustomerStats:
    """
    Attributes:
        name (str):
        uuid (UUID):
        latitude (float):
        longitude (float):
        score (float):
    """

    name: str
    uuid: UUID
    latitude: float
    longitude: float
    score: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid = str(self.uuid)

        latitude = self.latitude

        longitude = self.longitude

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uuid": uuid,
                "latitude": latitude,
                "longitude": longitude,
                "score": score,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        uuid = UUID(d.pop("uuid"))

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        score = d.pop("score")

        checklist_customer_stats = cls(
            name=name,
            uuid=uuid,
            latitude=latitude,
            longitude=longitude,
            score=score,
        )

        checklist_customer_stats.additional_properties = d
        return checklist_customer_stats

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
