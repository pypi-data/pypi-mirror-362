from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChecklistQuestion")


@_attrs_define
class ChecklistQuestion:
    """
    Attributes:
        uuid (UUID):
        category_uuid (UUID):
        description (Union[Unset, str]):
        solution (Union[None, Unset, str]): It is shown when incorrect or N/A answer is chosen
        correct_answer (Union[Unset, bool]):
        image (Union[None, Unset, str]):
    """

    uuid: UUID
    category_uuid: UUID
    description: Union[Unset, str] = UNSET
    solution: Union[None, Unset, str] = UNSET
    correct_answer: Union[Unset, bool] = UNSET
    image: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        category_uuid = str(self.category_uuid)

        description = self.description

        solution: Union[None, Unset, str]
        if isinstance(self.solution, Unset):
            solution = UNSET
        else:
            solution = self.solution

        correct_answer = self.correct_answer

        image: Union[None, Unset, str]
        if isinstance(self.image, Unset):
            image = UNSET
        else:
            image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "category_uuid": category_uuid,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if solution is not UNSET:
            field_dict["solution"] = solution
        if correct_answer is not UNSET:
            field_dict["correct_answer"] = correct_answer
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        category_uuid = UUID(d.pop("category_uuid"))

        description = d.pop("description", UNSET)

        def _parse_solution(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        solution = _parse_solution(d.pop("solution", UNSET))

        correct_answer = d.pop("correct_answer", UNSET)

        def _parse_image(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        image = _parse_image(d.pop("image", UNSET))

        checklist_question = cls(
            uuid=uuid,
            category_uuid=category_uuid,
            description=description,
            solution=solution,
            correct_answer=correct_answer,
            image=image,
        )

        checklist_question.additional_properties = d
        return checklist_question

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
