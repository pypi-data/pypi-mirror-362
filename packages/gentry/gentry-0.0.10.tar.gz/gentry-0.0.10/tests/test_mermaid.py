import pytest
from gentry.mermaid import Mermaid, Shape, Style
from gentry.tree import Tree

class DummyNode(Tree, Mermaid): ...

def test_mermaid_str_simple():
    node = DummyNode(label="A")
    result = str(node)
    assert "mermaid" in result
    assert "A" in result

def test_mermaid_str_with_properties():
    node = DummyNode(label="B", properties={"x": 1, "y": 2}, include_properties=True)
    result = str(node)
    assert "x=1" in result
    assert "y=2" in result

def test_mermaid_str_with_children():
    child = DummyNode(label="child")
    node = DummyNode(label="parent", children={"group": [child]})
    result = str(node)
    assert "parent" in result
    assert "child" in result
    assert "subgraph" in result

def test_mermaid_safe_escapes():
    assert Mermaid._mermaid_safe("-foo") == "\\\\-foo"
    assert Mermaid._mermaid_safe("+bar") == "\\\\+bar"
    assert Mermaid._mermaid_safe("baz") == "baz"

def test_mermaid_str_with_styles_and_shapes():
    node = DummyNode(label="C", shape=Shape.circle, style=Style.function)
    result = str(node)
    assert "shape: circle" in result
    assert "function" in result