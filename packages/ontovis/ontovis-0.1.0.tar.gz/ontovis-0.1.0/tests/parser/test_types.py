from ontovis.parser.types import Group

g1 = Group(name="test1", subgroups=[], path=[], fields=[])

test_groups = [Group(name=name) for name in ["test1", "test2", "test3"]]
subgroups1 = [Group(name=name) for name in ["sub1_1", "sub1_2"]]
subgroups2 = [Group(name=name) for name in ["sub2_1", "sub2_2"]]
test_groups[0].subgroups = subgroups1
test_groups[-1].subgroups = subgroups2


def test_find_group():
    assert Group.find_group(test_groups, "test1") is not None
    assert Group.find_group(test_groups, "sub1_1") is not None
    assert Group.find_group(test_groups, "sub2_2") is not None
    assert Group.find_group(test_groups, "NOEXIST") is None
