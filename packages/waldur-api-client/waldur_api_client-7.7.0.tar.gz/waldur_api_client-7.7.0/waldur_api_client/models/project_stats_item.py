from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectStatsItem")


@_attrs_define
class ProjectStatsItem:
    """
    Attributes:
        name (str):
        uuid (UUID):
        positive_count (int):
        negative_count (int):
        unknown_count (int):
        score (float):
    """

    name: str
    uuid: UUID
    positive_count: int
    negative_count: int
    unknown_count: int
    score: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        uuid = str(self.uuid)

        positive_count = self.positive_count

        negative_count = self.negative_count

        unknown_count = self.unknown_count

        score = self.score

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "uuid": uuid,
                "positive_count": positive_count,
                "negative_count": negative_count,
                "unknown_count": unknown_count,
                "score": score,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        uuid = UUID(d.pop("uuid"))

        positive_count = d.pop("positive_count")

        negative_count = d.pop("negative_count")

        unknown_count = d.pop("unknown_count")

        score = d.pop("score")

        project_stats_item = cls(
            name=name,
            uuid=uuid,
            positive_count=positive_count,
            negative_count=negative_count,
            unknown_count=unknown_count,
            score=score,
        )

        project_stats_item.additional_properties = d
        return project_stats_item

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
