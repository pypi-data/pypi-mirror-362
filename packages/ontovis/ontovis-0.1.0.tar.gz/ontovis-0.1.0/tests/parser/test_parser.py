from ontovis.io import read_local_or_remote
from ontovis.parser import build_groups, parse_pathbuilder
from ontovis.parser.strings import strip_prefix
from ontovis.parser.types import Field, Group


def test_strip_prefix():
    cases: list[dict[str, str | None]] = [
        {"input": "http://foo.bar/level/final", "expected": "final"},
        {"input": "./foo/bar/baz", "expected": "baz"},
        {"input": None, "expected": "<NO_ID>"},
    ]

    for case in cases:
        assert case["expected"] == strip_prefix(case["input"])


def test_empty_parse():
    root = read_local_or_remote("./tests/fixtures/fixture_empty.xml")
    paths = parse_pathbuilder(root)
    assert paths == []
    result = build_groups(paths)
    assert result == {}


def test_group_builder():
    root = read_local_or_remote("./tests/fixtures/fixture_group-hierarchy.xml")
    paths = parse_pathbuilder(root)
    result = build_groups(paths)

    expected = {
        "g_research_data_item": Group(
            name="g_research_data_item",
            subgroups=[
                Group(
                    name="g_research_data_item_title",
                    subgroups=[],
                    path=[
                        '"information_carrier"',
                        '"P102_has_title"',
                        '"alternative_title"',
                    ],
                    fields=[
                        Field(
                            name="f_research_data_item_title_appel",
                            path=[
                                '"information_carrier"',
                                '"P102_has_title"',
                                '"alternative_title"',
                                '"P1_is_identified_by"',
                                '"E41_Appellation"',
                            ],
                        ),
                        Field(
                            name="f_research_data_item_title_type",
                            path=[
                                '"information_carrier"',
                                '"P102_has_title"',
                                '"alternative_title"',
                                '"P2_has_type"',
                                '"E55_Type"',
                                '"P1_is_identified_by"',
                                '"E41_Appellation"',
                            ],
                        ),
                    ],
                )
            ],
            path=['"information_carrier"'],
            fields=[],
        )
    }
    assert result == expected
