from enum import StrEnum, auto


class Shape(StrEnum):
    rounded = auto()
    subprocess = auto()
    rect = auto()
    stadium = auto()
    cyl = auto()
    circle = auto()
    odd = auto()
    diamond = auto()
    hex = auto()
    braces = auto()
    doc = auto()
    delay = auto()
    tri = auto()
    docs = auto()
    processes = auto()
    flag = auto()
    none = auto()


class Style(StrEnum):
    none = auto()
    keyword = auto()
    loop = auto()
    function = auto()
    constant = auto()
    operator = auto()
    variable = auto()
    choice = auto()
    subgraph_even = auto()
    subgraph_odd = auto()


class Mermaid:
    """
    A mixin class for Tree that adds a __str__ method that will render a node and its children as markdown with mermaid.

    Assumes the existance of the following attributes:
      _children     a dict[str,list]
      label         a str
      properties    a dict
    """

    _style = Style.none
    _shape = Shape.rounded
    _include_properties = False

    def __init__(
        self,
        shape: (
            Shape | None
        ) = None,  # Shape and style can be overridden on a per instance basis as well
        style: Style | None = None,
        include_properties=None,
    ) -> None:
        """
        Initialize a Mermaid mixin instance.

        Args:
            shape (Shape | None): Optional. Override the default node shape for this instance.
            style (Style | None): Optional. Override the default node style for this instance.
            include_properties (bool | None): Optional. Whether to include properties in the node label.
        """
        self._ishape = shape
        self._istyle = style
        self._iinclude_properties = include_properties

    @staticmethod
    def _mermaid_safe(name: str) -> str:
        """
        Escape special characters in a node name for Mermaid compatibility.

        Args:
            name (str): The node name to escape.

        Returns:
            str: The escaped node name.
        """
        if name[0] in "-+*":
            return f"\\\\{name}"
        return name

    _index: int = 0

    styles: dict[Style, str] = {
        Style.none: "",
        Style.keyword: "fill:#dFd",
        Style.function: "fill:#bff,font-size:20px,stroke-width:2px,font-weight:bold",
        Style.loop: "fill:#fdd",
        Style.operator: "font-weight:bold,font-size:20px",
        Style.constant: "color:#3a3",
        Style.variable: "color:#a33",
        Style.subgraph_even: "fill:#eff",
        Style.subgraph_odd: "fill:#eee",
    }

    def __str__(self, parent_index=0) -> str:
        """
        Render the node and its children as a Mermaid markdown graph.

        Args:
            parent_index (int): The index of the parent node, used for indentation and unique node IDs.

            this is used internally when recursing into the tree.

        Returns:
            str: The Mermaid markdown representation of the tree rooted at this node.
        """

        # calculate the left hand part (or parent)
        # we are very conservative with what a label can be, even though it is supposed to be a string
        node_name = self.__class__.__name__
        if hasattr(self, "label") and self.label is not None:
            name = str(self.label)
        else:
            name = node_name

        sep = ",\\n"  # for f-strings prior to python 3.13 we need to take the backslash out of the string
        nl = "\\n"
        include_properties = self._include_properties  # class var
        if (
            self._iinclude_properties is not None
        ):  # override if instance variable is not None
            include_properties = self._iinclude_properties
        if include_properties:  # neither None or False
            props = [f"{k}={v}" for k, v in self.properties.items()]
            props = f"{nl}({sep.join(props)})"
        else:
            props = ""

        name = f"{name}{props}"

        indent = "    " * (parent_index + 1)
        pstyle = self._style
        if self._istyle is not None:
            pstyle = self._istyle
        if pstyle is None or pstyle is Style.none:
            style = ""
        else:
            style = f":::{pstyle}"

        pshape = self._shape
        if self._ishape is not None:
            pshape = self._ishape
        if pshape is None or pshape is Shape.none:
            pshape = Shape.rounded

        # calculate the right hand parts (or children)
        cs = []

        subgraphstyle = Style.subgraph_even if parent_index % 2 else Style.subgraph_odd

        if self.is_leaf() and parent_index == 0:
            p = f'{node_name}{parent_index}{style}@{{shape: {pshape}, label: "{self._mermaid_safe(name)}"}}'

            cs.append(p)
        else:
            p = f'{node_name}{parent_index}{style}@{{shape: {pshape}, label: "{self._mermaid_safe(name)}"}}'
            for group, children in self._children.items():
                groupid = f"subgraph{Mermaid._index}"
                Mermaid._index += 1
                groupstart = f"subgraph {groupid}[{group}]"

                cs.append(
                    f"{indent}{groupid}:::{subgraphstyle}\n{indent}{p} --> {groupid}\n{indent}{groupstart}\n{indent}        direction TB\n"
                )

                for i, child in enumerate(children):
                    if child is None:
                        continue
                    Mermaid._index += 1

                    node_name = child.__class__.__name__
                    if hasattr(child, "label") and child.label is not None:
                        childname = str(child.label)
                    else:
                        childname = node_name

                    include_properties = child._include_properties  # class var
                    if (
                        child._iinclude_properties is not None
                    ):  # override if instance variable is not None
                        include_properties = child._iinclude_properties
                    if include_properties:  # neither None or False
                        props = [f"{k}={v}" for k, v in child.properties.items()]
                        props = f"{nl}({sep.join(props)})"
                    else:
                        props = ""

                    childname = f"{childname}{props}"

                    cstyle = child._style
                    if child._istyle is not None:
                        cstyle = child._istyle
                    if cstyle is None or cstyle is Style.none:
                        childstyle = ""
                    else:
                        childstyle = f":::{cstyle}"

                    cshape = child._shape
                    if child._ishape is not None:
                        cshape = child._ishape
                    if cshape is None or cshape is Shape.none:
                        cshape = Shape.rounded

                    if child.is_leaf():
                        c = f'{indent}{child.__class__.__name__}{self._index}{childstyle}@{{shape: {cshape}, label: "{self._mermaid_safe(childname)}"}}'
                        cs.append(c)
                    else:
                        cs.append(child.__str__(parent_index=parent_index + 1))

                cs.append(f"{indent}end")

        prolog = ""
        epilog = ""
        styles = "\n\t".join(
            f"classDef {style} {definition}"
            for style, definition in self.styles.items()
            if style != "none"
        )
        if parent_index == 0:
            prolog = f"```mermaid\ngraph TD\n\t{styles}\n\n"
            epilog = "\n```"

        return prolog + ("\n".join(cs)) + epilog
