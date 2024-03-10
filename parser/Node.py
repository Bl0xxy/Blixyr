from typing import Any
from enum import Enum

class NodeType(Enum):
    ProgramNode = 0
    ActionNode = 1
    ValueNode = 2
    ConvertNode = 3

    StringNode = 4
    BytesNode = 5
    VarAccNode = 6

    PrintNode = 7
    VarDecNode = 8
    VarModNode = 9

    StringConvertNode = 10
    BytesConvertNode = 11

    InputNode = 12
    GetchNode = 13
    FlushNode = 14

    BoolNode = 15
    NumberNode = 16

    WaitNode = 17
    
    FuncDecNode = 18
    FuncCallNode = 19
    FuncNode = 20

    ListNode = 21

    PythonNode = 22
    ImportNode = 23

class Node:
    def __init__(self, type: NodeType, children: list[Any]) -> None:
        self.type: NodeType = type
        self.children: list[Any] = children

    def __repr__(self) -> str:
        return f'Returned Node object type "{self.type.name}" and children {str(self.children)}'
    
class ProgramNode(Node):
    def __init__(self, children: list[Node]) -> None:
        super().__init__(type, children)

class ActionNode(Node):
    def __init__(self, children: list[Node], type: NodeType = NodeType.ActionNode) -> None:
        super().__init__(type, children)

class ValueNode(Node):
    def __init__(self, value: Any, type: NodeType = NodeType.ValueNode) -> None:
        super().__init__(type, [value])

    def __str__(self) -> str:
        if isinstance(self.children[0], list):
            return f'[{','.join()}]'

class ConvertNode(ActionNode):
    def __init__(self, identifier: str, convert_to: NodeType, type: NodeType = NodeType.ConvertNode) -> None:
        super().__init__([identifier, convert_to], type)

class StringNode(ValueNode):
    def __init__(self, value: str) -> None:
        super().__init__(value, NodeType.StringNode)

class BytesNode(ValueNode):
    def __init__(self, value: bytes) -> None:
        super().__init__(value, NodeType.BytesNode)

class BoolNode(ValueNode):
    def __init__(self, value: bool) -> None:
        super().__init__(value, NodeType.BoolNode)

class NumberNode(ValueNode):
    def __init__(self, value: int) -> None:
        super().__init__(value, NodeType.NumberNode)

class VarAccNode(ValueNode):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, NodeType.VarAccNode)

class StringConvertNode(ConvertNode):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, NodeType.StringNode, NodeType.StringConvertNode)

class BytesConvertNode(ConvertNode):
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier, NodeType.BytesNode, NodeType.BytesConvertNode)

class PrintNode(ActionNode):
    def __init__(self, text: StringNode, flush: BoolNode = BoolNode(False)) -> None:
        super().__init__([text, flush], NodeType.PrintNode)

class InputNode(ActionNode):
    def __init__(self, identifier: str = '') -> None:
        super().__init__([identifier], NodeType.InputNode)

class GetchNode(ActionNode):
    def __init__(self, identifier: str = '') -> None:
        super().__init__([identifier], NodeType.GetchNode)

class VarDecNode(ActionNode):
    def __init__(self, identifier: str, value: ValueNode = None) -> None:
        super().__init__([identifier, value], NodeType.VarDecNode)

class VarModNode(ActionNode):
    def __init__(self, identifier: str, value: ValueNode) -> None:
        super().__init__([identifier, value], NodeType.VarModNode)

class WaitNode(ActionNode):
    def __init__(self, wait_time: NumberNode) -> None:
        super().__init__([wait_time], NodeType.WaitNode)

class FuncCallNode(ActionNode):
    def __init__(self, identifier: str, args: dict[ValueNode]) -> None:
        super().__init__([identifier, args], NodeType.FuncCallNode)

class FuncNode(ValueNode):
    def __init__(self, value: Any, type: NodeType = NodeType.ValueNode) -> None:
        super().__init__(value, NodeType.FuncNode)

class ListNode(ValueNode):
    def __init__(self, value: list, type: NodeType = NodeType.ListNode) -> None:
        super().__init__(value, type)

class PythonNode(ActionNode):
    def __init__(self, line: StringNode, safe: bool = False, type: NodeType = NodeType.PythonNode) -> None:
        super().__init__([line, safe], type)

class ImportNode(ActionNode):
    def __init__(self, module_name: str, type: NodeType = NodeType.ImportNode) -> None:
        super().__init__([module_name], type)