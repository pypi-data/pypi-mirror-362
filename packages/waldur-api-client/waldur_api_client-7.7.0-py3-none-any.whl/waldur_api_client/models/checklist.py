from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Checklist")


@_attrs_define
class Checklist:
    """
    Attributes:
        uuid (UUID):
        name (str):
        questions_count (int):
        category_name (str):
        category_uuid (UUID):
        roles (list[str]):
        description (Union[Unset, str]):
    """

    uuid: UUID
    name: str
    questions_count: int
    category_name: str
    category_uuid: UUID
    roles: list[str]
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        questions_count = self.questions_count

        category_name = self.category_name

        category_uuid = str(self.category_uuid)

        roles = self.roles

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "questions_count": questions_count,
                "category_name": category_name,
                "category_uuid": category_uuid,
                "roles": roles,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        questions_count = d.pop("questions_count")

        category_name = d.pop("category_name")

        category_uuid = UUID(d.pop("category_uuid"))

        roles = cast(list[str], d.pop("roles"))

        description = d.pop("description", UNSET)

        checklist = cls(
            uuid=uuid,
            name=name,
            questions_count=questions_count,
            category_name=category_name,
            category_uuid=category_uuid,
            roles=roles,
            description=description,
        )

        checklist.additional_properties = d
        return checklist

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
