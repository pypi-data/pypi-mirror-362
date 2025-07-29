# pyright: strict
import xml.etree.ElementTree as ET


def read_local_or_remote(file: str) -> ET.Element:
    if file.startswith("http") or file.startswith("https"):
        from requests import get as requests_get

        response = requests_get(file)
        root = ET.fromstring(response.text)
    else:
        tree = ET.parse(file)
        root = tree.getroot()

    return root
