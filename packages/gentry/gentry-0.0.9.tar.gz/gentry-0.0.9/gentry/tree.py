from collections import defaultdict

class _MetaTree(type):
    """
    Ensures that when subclassing Tree, any _groups class variable will be initialized
    with a set of strings that are valid python identifiers that do not start with an underscore.
    """
    def __new__(cls, clsname, bases, attrs, **kwargs):
        if "_groups" in attrs:
            value = attrs["_groups"]
            if not isinstance(value, set):
                raise AttributeError(f"_groups attribute is not a set")
            for group in value:
                if not isinstance(group, str):
                    raise AttributeError(f"_groups item {group} is not a str")
                elif group.startswith("_"):
                    raise AttributeError(f"_groups item {group} starts with underscore")
                elif not group.isidentifier():
                    raise AttributeError(f"_groups item {group} not a valid python identifier")
                elif group in {"label", "properties"}:
                    raise AttributeError(f"_groups item {group} is a reserved name")
        return super().__new__(cls, clsname, bases, attrs, **kwargs)
   
class Tree(metaclass=_MetaTree):
    """
    A basic Tree object has one attribute "children" which is a defaultdict.

    The keys are group names, the values are lists of Tree objects.

    If the children argument is given, it must be a defaultdict or it will be converted to one.

    If any keys to the children dict are also in the groups set, these keys can also be used as attributes
    to directly access the values in the children dictionary.

    This setup allows for mixin classes and generic tools like a visitor to rely on the presence of a children
    dict that doesn't change if a Tree class is inherited, yet allow for a more semantically meaningful way of
    accessing groups of children im derived classes.
    """

    _groups = set()

    def __init__(
        self,
        label: str,
        children: (
            defaultdict[str, list["Tree"]] | dict[str, list["Tree"]] | None
        ) = None,
        properties: dict|None = None,
        *args, **kwargs
    ):
        self.label = label
        self._children: defaultdict[str, list[Tree]] = (
            defaultdict(list) if children is None else defaultdict(list, **children)
        )
        self.properties = {} if properties is None else properties
        super(Tree, self).__init__(*args, *kwargs)   # executes next __init__() in MRO, see: https://stackoverflow.com/a/6099026

    def __getattr__(self, name: str) -> "list[Tree]":
        """
        Called when the default attribute access fails.

        We then check if we should redirect this access to the children attribute.
        """
        if name in self._groups:
            return self._children[name]
        raise AttributeError(f"{name} attribute could not be found on {self!r}")

    def __setattr__(self, name, value):
        """
        Called when an attribute assignment is attempted.

        If name is in groups, we redirect this access to the children attribute.
        IF it is redirected, we check if the value is a list.
        """
        if name in self._groups:
            if isinstance(value, list):
                self._children[name] = value
            else:
                raise AttributeError(f"{name} {type(value)} is not a list")
        else:
            object.__setattr__(self, name, value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(label={self.label}, groups={self._groups})"

    def is_leaf(self) -> bool:
        return sum(len(group) for group in self._children.values()) == 0

class Visitor:
    def __init__(self, root: Tree, strict: bool = False) -> None:
        self.root = root
        self.strict = strict
        self.result = None

    def visit(self):
        self.result = self._visit(self.root)
        return self.result

    def _get_visitor(self, tree: Tree):
        typename = tree.__class__.__name__
        for klass in self.__class__.__mro__:
            generic_visitor = f"_do_{klass.__name__.lower()}"
            visitor = f"{generic_visitor}_{typename}"
            if hasattr(self, visitor):
                return getattr(self, visitor)
            elif not self.strict and hasattr(self, generic_visitor):
                return getattr(self, generic_visitor)
        raise NotImplementedError(
            f"class {self.__class__.__name__} missing {visitor} and {generic_visitor} methods."
        )

    # children first, then self (bottom-up a.k.a. breadth-first)
    def _visit(self, tree: Tree):
        typename = tree.__class__.__name__
        results: defaultdict[str, list] = defaultdict(list)
        for group, children in tree._children.items():
            for child in children:
                results[group].append(self._visit(child))

        result = self._get_visitor(tree)(tree)
        return {typename: result, "children": results}


class Count(Visitor):
    def _do_count(self, tree: Tree):
        return 1

    @staticmethod
    def _sum(d):
        total = 0
        match (d):
            case dict(mapping):
                total += sum(Count._sum(v) for v in d.values())
            case list(iterable):
                total += sum(Count._sum(v) for v in d)
            case int(value):
                total += value
        return total

    def count(self):
        results = self.visit()
        # print(json.dumps(results, indent=4))
        return self._sum(results)


if __name__ == "__main__":

    class A(Tree):
        _groups = {"left", "right"}

    class B(
        A
    ):  # specialized version of A, but should still function the same with regard to group names
        ...

    root = A(label="root")
    left = A(label="left")
    right = A(label="right")
    root.left.append(left)
    root.right = [right]

    root.aaa = 42
    print(root.left)
    print(root.right)
    print(root.label)
    print(root.aaa)
    try:
        print(root.bbb)
    except AttributeError:
        ...

    root = B(label="root")
    left = B(label="left")
    right = B(label="right")
    root.left.append(left)
    root.right = [right]

    root.aaa = 42
    print(root.left)
    print(root.right)
    print(root.label)
    print(root.aaa)
    try:
        print(root.bbb)
    except AttributeError:
        ...
