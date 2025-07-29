import pathlib


def strip_prefix(s: str | None) -> str:
    if s is None:
        return "<NO_ID>"

    return pathlib.Path(s).name
