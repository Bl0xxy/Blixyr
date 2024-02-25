from typing import Any
from enum import Enum

class NodeType(Enum):
    VarDecNode = 0
    VarAccNode = 1
    PrintNode = 2
    ValueNode = 3
    StringNode = 4
    InputNode = 5
    GetchNode = 6
    BytesNode = 7
    StringConvertNode = 8

class Node:
    def __init__(self, type: NodeType, values: list[Any]) -> None:
        self.type: NodeType = type
        self.values: list[Any] = values

    def __repr__(self) -> str:
        return f"Returned Node object type \"{self.type.name}\" and values \"{str(self.values)}\""
    
class ValueNode(Node):
    def __init__(self, value: Any, type: NodeType = NodeType.ValueNode) -> None:
        super().__init__(type, [value])
    
class StringNode(ValueNode):
    def __init__(self, value: str) -> None:
        super().__init__(value, NodeType.StringNode)

class VarDecNode(Node):
    def __init__(self, identifier: str, value: Any) -> None:
        super().__init__(NodeType.VarDecNode, [identifier, value])

class VarAccNode(ValueNode):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, type = NodeType.VarAccNode)

class PrintNode(Node):
    def __init__(self, text: StringNode, newline: bool) -> None:
        super().__init__(NodeType.PrintNode, [text, newline])

class InputNode(Node):
    def __init__(self, identifier: str) -> None:
        super().__init__(NodeType.InputNode, [identifier])

class GetchNode(Node):
    def __init__(self, identifier: str) -> None:
        super().__init__(NodeType.GetchNode, [identifier])

class BytesNode(ValueNode):
    def __init__(self, value: bytes) -> None:
        super().__init__(value, type = NodeType.BytesNode)

class StringConvertNode(Node):
    def __init__(self, identifier: str) -> None:
        super().__init__(NodeType.StringConvertNode, [identifier])