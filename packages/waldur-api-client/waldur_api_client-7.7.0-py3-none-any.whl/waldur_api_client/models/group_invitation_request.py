from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupInvitationRequest")


@_attrs_define
class GroupInvitationRequest:
    """
    Attributes:
        role (UUID):
        scope (str):
        auto_create_project (Union[Unset, bool]): Create project and grant project permissions instead of customer
            permissions
        project_name_template (Union[Unset, str]): Template for project name. Supports {username}, {email}, {full_name}
            variables
        project_role (Union[None, UUID, Unset]):
    """

    role: UUID
    scope: str
    auto_create_project: Union[Unset, bool] = UNSET
    project_name_template: Union[Unset, str] = UNSET
    project_role: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = str(self.role)

        scope = self.scope

        auto_create_project = self.auto_create_project

        project_name_template = self.project_name_template

        project_role: Union[None, Unset, str]
        if isinstance(self.project_role, Unset):
            project_role = UNSET
        elif isinstance(self.project_role, UUID):
            project_role = str(self.project_role)
        else:
            project_role = self.project_role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
                "scope": scope,
            }
        )
        if auto_create_project is not UNSET:
            field_dict["auto_create_project"] = auto_create_project
        if project_name_template is not UNSET:
            field_dict["project_name_template"] = project_name_template
        if project_role is not UNSET:
            field_dict["project_role"] = project_role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = UUID(d.pop("role"))

        scope = d.pop("scope")

        auto_create_project = d.pop("auto_create_project", UNSET)

        project_name_template = d.pop("project_name_template", UNSET)

        def _parse_project_role(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                project_role_type_0 = UUID(data)

                return project_role_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        project_role = _parse_project_role(d.pop("project_role", UNSET))

        group_invitation_request = cls(
            role=role,
            scope=scope,
            auto_create_project=auto_create_project,
            project_name_template=project_name_template,
            project_role=project_role,
        )

        group_invitation_request.additional_properties = d
        return group_invitation_request

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
