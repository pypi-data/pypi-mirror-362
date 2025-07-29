# pyright: strict
from collections.abc import Iterable
from xml.etree.ElementTree import Element

from .typed_accessors import get_path_array, safe_get_bool, safe_get_text
from .types import Field, Group, Path


def parse_pathbuilder(document: Element) -> list[Path]:
    out: list[Path] = []
    paths = document.findall("path")
    if paths == []:
        return []

    for path in paths:
        enabled = safe_get_bool(path, "./enabled")
        path_id = safe_get_text(path, "./id")
        is_group = safe_get_bool(path, "./is_group")
        group_id = safe_get_text(path, "./group_id")
        if group_id == "0":
            group_id = None

        path_array = get_path_array(path)

        out.append(Path(enabled, path_id, is_group, group_id, path_array))

    return out


def build_groups(paths: Iterable[Path], skip_disabled: bool = True) -> dict[str, Group]:
    all_groups: dict[str, Group] = {}
    top_level_groups: dict[str, Group] = {}

    # first pass: assemble all group instances
    for path in paths:
        if skip_disabled and not path.enabled:
            continue

        if not path.is_group:
            continue

        # the defaultdict will create an empty group we can use
        group = Group(name=path.path_id, path=path.path_array)
        all_groups[path.path_id] = group

        if path.group_id is None:
            top_level_groups[path.path_id] = group

    groups: dict[str, Group] = {}

    for path in paths:
        if skip_disabled and not path.enabled:
            continue

        if path.is_group:
            if path.group_id is None:
                # The current path does not reference a parent group: it is a
                # top-level container, and has been processed in the first pass.
                groups[path.path_id] = top_level_groups[path.path_id]
                continue

            group = all_groups[path.path_id]

            # The current path has a parent group, which definitely exists in
            # `all_groups`, and may already exist in `groups`. Check which case we
            # are in, and use the appropriate group.
            if path.group_id in groups:
                parent_group = groups[path.group_id]
            elif path.group_id in all_groups:
                parent_group = all_groups[path.group_id]
            else:
                raise Exception(
                    f"group with id {path.group_id} not found. This should not happen."
                )

            parent_group.subgroups.append(group)

            continue

        if path.group_id in groups:
            parent_group = groups[path.group_id]
        elif path.group_id in all_groups:
            parent_group = all_groups[path.group_id]
        else:
            raise Exception(
                f"group with id {path.group_id} not found. This should not happen."
            )

        # the path is a field, so append it to the correct group
        assert path.group_id is not None
        parent_group.fields.append(Field(name=path.path_id, path=path.path_array))

    return groups
