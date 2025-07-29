from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List

from rich.tree import Tree


class NodeType(Enum):
    FILE = "file"
    FOLDER = "folder"
    REPOSITORY = "project"


@dataclass
class Node:
    name: str
    description: str
    node_type: NodeType

    children: List["Node"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_string(self, indent: int = 0) -> str:
        spacer = " " * indent
        lines = [f"{spacer}{self.name} ({self.node_type.value}): {self.description}"]
        for child in self.children:
            lines.append(child.to_string(indent + 4))
        return "\n".join(lines)

    def to_tree(self) -> Tree:
        return build_rich_tree(self)

    def print(self, indent: int = 0) -> None:
        print(self.to_string(indent))

    def add_children(self, children: "Node") -> None:
        self.children.append(children)


def get_icon(node_type: NodeType):
    return {
        NodeType.FILE: "📄",
        NodeType.FOLDER: "📁",
        NodeType.REPOSITORY: "🧩",
    }.get(node_type, "❓")


def build_rich_tree(node: Node):
    icon = get_icon(node.node_type)
    label = f"{icon} [bold]{node.name}[/] ([dim]{node.node_type.value}[/]): {node.description}"
    tree = Tree(label)
    for child in node.children:
        tree.add(build_rich_tree(child))
    return tree
