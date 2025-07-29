from xml.etree.ElementTree import Element

from .strings import strip_prefix


def safe_get_text(path: Element, xpath: str) -> str:
    thing = path.find(xpath)
    assert thing is not None and thing.text is not None

    return thing.text


def safe_get_bool(path: Element, xpath: str) -> bool:
    thing = path.find(xpath)
    assert thing is not None and thing.text is not None

    return thing.text == "1"


def get_path_array(path: Element) -> list[str]:
    path_array = path.find("./path_array")
    assert path_array is not None
    path_array = [strip_prefix(particle.text) for particle in path_array]

    # remove the main URL part of the path particle
    path_array = [strip_prefix(particle) for particle in path_array]
    # TODO: move this quoting into the template
    path_array = [f'"{x}"' for x in path_array]

    return path_array
