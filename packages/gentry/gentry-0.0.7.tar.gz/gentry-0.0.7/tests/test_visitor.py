import pytest
from collections import defaultdict
from gentry.tree import Tree, Visitor, Count


class DummyTree(Tree):
    groups = {"children"}


class DummyVisitor(Visitor):
    def _do_dummyvisitor(self, tree):
        return f"visited:{tree.label}"


def make_simple_tree():
    # root
    # ├── left
    # └── right
    class MyTree(Tree):
        _groups = {"left", "right"}

    left = MyTree(label="left")
    right = MyTree(label="right")
    root = MyTree(label="root")
    root.left.append(left)
    root.right.append(right)
    return root, left, right


def test_visitor_basic():
    root, left, right = make_simple_tree()

    class MyVisitor(Visitor):
        def _do_myvisitor(self, tree):
            return f"visited:{tree.label}"

    v = MyVisitor(root)
    result = v.visit()
    assert "MyTree" in result
    assert result["MyTree"] == "visited:root"
    assert "children" in result
    assert "left" in result["children"]
    assert "right" in result["children"]


def test_visitor_get_visitor_strict():
    root, _, _ = make_simple_tree()

    class MyVisitor(Visitor):
        def _do_myvisitor_MyTree(self, tree):
            return "ok"

    v = MyVisitor(root, strict=True)
    result = v.visit()
    assert result['MyTree'] == "ok"
    left_child_group = result['children']["left"]
    assert len(left_child_group) == 1
    assert left_child_group[0]['MyTree'] == "ok"
    right_child_group = result['children']["right"]
    assert len(right_child_group) == 1
    assert right_child_group[0]['MyTree'] == "ok"


def test_visitor_get_visitor_missing():
    root, _, _ = make_simple_tree()

    class MyVisitor(Visitor):
        pass

    v = MyVisitor(root, strict=True)
    with pytest.raises(NotImplementedError):
        v._get_visitor(root)


def test_visit_returns_expected_structure():
    root, left, right = make_simple_tree()

    class MyVisitor(Visitor):
        def _do_myvisitor(self, tree):
            return tree.label

    v = MyVisitor(root)
    result = v.visit()
    assert result["MyTree"] == "root"
    assert result["children"]["left"][0]["MyTree"] == "left"
    assert result["children"]["right"][0]["MyTree"] == "right"


def test_count_simple_tree():
    root, left, right = make_simple_tree()
    c = Count(root)
    assert c.count() == 3  # root + left + right


def test_count_nested_tree():
    class MyTree(Tree):
        groups = {"children"}

    leaf1 = MyTree(label="leaf1")
    leaf2 = MyTree(label="leaf2")
    mid = MyTree(label="mid", children={"children": [leaf1, leaf2]})
    root = MyTree(label="root", children={"children": [mid]})
    c = Count(root)
    assert c.count() == 4  # root, mid, leaf1, leaf2


def test_count_empty_tree():
    t = Tree(label="root")
    c = Count(t)
    assert c.count() == 1


def test_count_with_subclass():
    class MyTree(Tree):
        groups = {"children"}

    t = MyTree(label="root")
    c = Count(t)
    assert c.count() == 1


def test_count_sum_handles_various_types():
    # Test _sum with int, list, dict
    assert Count._sum(5) == 5
    assert Count._sum([1, 2, 3]) == 6
    assert Count._sum({"a": 1, "b": 2}) == 3
    nested = {"a": [1, 2], "b": {"c": 3}}
    assert Count._sum(nested) == 6
