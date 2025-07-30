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
        """
        Initialize a Tree node.

        When subclassing you can initialize the class variabel `_groups` to a set of strings.
        Any string in that set can then be used as an attribute of the node and will be used
        as a key of the `_children` attribute.

        Args:
            label (str): The label for this node.
            children (defaultdict|dict|None): Optional. A mapping from group names to lists of child Tree nodes.
                If None, an empty defaultdict is used.
            properties (dict|None): Optional. Arbitrary properties for this node.
            args: Additional arguments for multiple inheritance.
            kwargs: Additional keyword arguments for multiple inheritance.
        """
        self.label = label
        self._children: defaultdict[str, list[Tree]] = (
            defaultdict(list) if children is None else defaultdict(list, **children)
        )
        self.properties = {} if properties is None else properties
        super(Tree, self).__init__(*args, **kwargs)   # executes next __init__() in MRO, see: https://stackoverflow.com/a/6099026

    def __getattr__(self, name: str) -> "list[Tree]":
        """
        Called when the default attribute access fails.

        If the attribute name is in the _groups set, return the corresponding list of children from _children.
        Otherwise, raise AttributeError.

        Args:
            name (str): The attribute name.

        Returns:
            list[Tree]: The list of child nodes for the group.

        Raises:
            AttributeError: If the attribute is not found and is also not a group.
        """
        if name in self._groups:
            return self._children[name]
        raise AttributeError(f"{name} attribute could not be found on {self!r}")

    def __setattr__(self, name, value):
        """
        Called when an attribute assignment is attempted.

        If the attribute name is in _groups, set the corresponding group in _children to the given value,
        which must be a list. Otherwise, set the attribute normally.

        Args:
            name (str): The attribute name.
            value: The value to assign.

        Raises:
            AttributeError: If assigning a non-list to a group attribute.
        """
        if name in self._groups:
            if isinstance(value, list):
                self._children[name] = value
            else:
                raise AttributeError(f"{name} {type(value)} is not a list")
        else:
            object.__setattr__(self, name, value)

    def __repr__(self) -> str:
        """
        Return a string representation of the Tree node.

        Returns:
            str: The string representation.
        """
        return f"{self.__class__.__name__}(label={self.label}, groups={self._groups})"

    def is_leaf(self) -> bool:
        """
        Check if the node is a leaf (i.e., has no children in any group).

        Returns:
            bool: True if the node has no children, False otherwise.
        """
        return sum(len(group) for group in self._children.values()) == 0

class Visitor:
    def __init__(self, root: Tree, strict: bool = False) -> None:
        """
        Initialize the Visitor.

        Args:
            root (Tree): The root node to start visiting from.
            strict (bool): If True, require exact visitor method matches for each node type.
        """
        self.root = root
        self.strict = strict
        self.result = None

    def visit(self):
        """
        Start the visiting process from the root node.

        Returns:
            The result of visiting the root node.
        """
        self.result = self._visit(self.root)
        return self.result

    def _get_visitor(self, tree: Tree):
        """
        Find the appropriate visitor method for the given tree node.

        When we visit a node the name of the visitor node will be constructed from the class
        name and the lower case class name of the visitor class. So if our Visitor derived
        class is called Validator and we encounter an instance of Person, the visitor we will be
        looking for is `_do_validator_Person`

        If that method cannot be found, we will look for a generic visitor `_do_validator()`,
        unless the visitor class was instantiated with `strict=True`.

        If no visitor method was found, we follow the method resolution order to see if we can
        find one in one of the superclassed. So if `Person` was derived from `Entity`, we would
        look for `_do_validator_Entity()` next.

        Args:
            tree (Tree): The node to find a visitor for.

        Returns:
            Callable: The visitor method.

        Raises:
            NotImplementedError: If no suitable visitor method is found.
        """
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

    def _visit(self, tree: Tree):
        """
        Recursively visit the tree in a bottom-up (children first) manner.

        Args:
            tree (Tree): The node to visit.

        Returns:
            dict: A dictionary containing the results for this node and its children.
        """
        typename = tree.__class__.__name__
        results: defaultdict[str, list] = defaultdict(list)
        for group, children in tree._children.items():
            for child in children:
                results[group].append(self._visit(child))

        result = self._get_visitor(tree)(tree)
        return {typename: result, "children": results}


class Count(Visitor):
    def _do_count(self, tree: Tree):
        """
        Visitor method for counting a single node.

        Args:
            tree (Tree): The node being counted.

        Returns:
            int: Always returns 1 for each node.
        """
        return 1

    @staticmethod
    def _sum(d):
        """
        Recursively sum up all integer values in a nested structure of dicts and lists.

        Args:
            d: The nested structure (dict, list, or int).

        Returns:
            int: The total sum of all integers found.
        """
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
        """
        Count the total number of nodes in the tree.

        Returns:
            int: The total node count.
        """
        results = self.visit()
        return self._sum(results)


if __name__ == "__main__": # pragma: no cover

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
