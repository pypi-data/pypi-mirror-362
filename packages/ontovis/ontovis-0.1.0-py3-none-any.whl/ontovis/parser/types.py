from collections.abc import Iterable
from dataclasses import dataclass, field


@dataclass
class Path:
    enabled: bool
    path_id: str
    is_group: bool
    group_id: str | None
    path_array: list[str] = field(default_factory=list)


@dataclass
class Field:
    name: str
    path: list[str] = field(default_factory=list)


@dataclass
class Group:
    name: str
    subgroups: list["Group"] = field(default_factory=list)
    path: list[str] = field(default_factory=list)
    fields: list[Field] = field(default_factory=list)

    @classmethod
    def find_group(cls, groups: Iterable["Group"], group_id: str) -> "Group | None":
        for group in groups:
            if group.name == group_id:
                return group

        for group in groups:
            hit = Group.find_group(group.subgroups, group_id)
            if hit is not None:
                return hit

        return None
