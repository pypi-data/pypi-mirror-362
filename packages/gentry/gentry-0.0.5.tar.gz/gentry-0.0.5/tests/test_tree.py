import pytest
from collections import defaultdict
from gentry.tree import Tree


class TestTree:
    def test_init_default_children(self):
        t = Tree(label="root")
        assert t.label == "root"
        assert isinstance(t._children, defaultdict)
        assert t._children == {}

    def test_init_with_children_dict(self):
        child = Tree(label="child")
        children = {"group1": [child]}
        t = Tree(label="root", children=children)
        assert t._children["group1"] == [child]

    def test_init_with_children_defaultdict(self):
        child = Tree(label="child")
        children = defaultdict(list, {"group1": [child]})
        t = Tree(label="root", children=children)
        assert t._children["group1"] == [child]

    def test_getattr_group(self):
        class MyTree(Tree):
            _groups = {"group1"}

        t = MyTree(label="root")
        c = MyTree(label="child")
        t.group1.append(c)
        assert t.group1 == [c]

    def test_getattr_non_group_raises(self):
        t = Tree(label="root")
        with pytest.raises(AttributeError):
            _ = t.nonexistent

    def test_setattr_group(self):
        class MyTree(Tree):
            _groups = {"group1"}

        t = MyTree(label="root")
        c = MyTree(label="child")
        t.group1 = [c]
        assert t._children["group1"] == [c]

    def test_setattr_group_non_list_raises(self):
        class MyTree(Tree):
            _groups = {"group1"}

        t = MyTree(label="root")
        with pytest.raises(AttributeError):
            t.group1 = "notalist"

    def test_setattr_normal(self):
        t = Tree(label="root")
        t.foo = 123
        assert t.foo == 123

    def test_repr(self):
        t = Tree(label="root")
        r = repr(t)
        assert "Tree" in r and "label=root" in r

    def test_groups_inheritance(self):
        class A(Tree):
            _groups = {"left", "right"}

        class B(A):
            pass

        b = B(label="b")
        l = B(label="left")
        r = B(label="right")
        b.left.append(l)
        b.right = [r]
        assert b.left == [l]
        assert b.right == [r]

    def test_subclass_with_own_groups(self):
        class Base(Tree):
            _groups = {"foo"}

        class Sub(Base):
            _groups = {"bar"}

        s = Sub(label="s")
        b = Sub(label="bar")
        s.bar.append(b)
        assert s.bar == [b]
        # foo should not be a group in Sub
        with pytest.raises(AttributeError):
            _ = s.foo

    def test_subclass_invalid_groups_type(self):
        with pytest.raises(AttributeError):

            class Bad(Tree):
                _groups = ["not", "a", "set"]

    def test_subclass_groups_with_invalid_names(self):
        with pytest.raises(AttributeError):

            class Bad(Tree):
                _groups = {"_bad"}

        with pytest.raises(AttributeError):

            class Bad2(Tree):
                _groups = {"not-valid!"}

        with pytest.raises(AttributeError):

            class Bad3(Tree):
                _groups = {123}

    def test_subclass_groups_are_independent(self):
        class A(Tree):
            _groups = {"left"}

        class B(Tree):
            _groups = {"right"}

        a = A(label="a")
        b = B(label="b")
        l = A(label="left")
        r = B(label="right")
        a.left.append(l)
        b.right.append(r)
        assert a.left == [l]
        assert b.right == [r]
        with pytest.raises(AttributeError):
            _ = a.right
        with pytest.raises(AttributeError):
            _ = b.left
        assert b.right == [r]

    def test_is_leaf(self):
        class MyTree(Tree):
            _groups = {"kids"}

        # A node with no children should be a leaf
        t = MyTree(label="root")
        assert t.is_leaf()

        # A node with one child in a group shouldn't be a leaf
        child = MyTree(label="child")
        t.kids.append(child)
        assert not t.is_leaf()

        # A node with multiple children in multiple groups
        t2 = MyTree(label="root2")
        t2.kids.append(MyTree(label="c1"))
        t2.kids.append(MyTree(label="c2"))
        assert not t2.is_leaf()
