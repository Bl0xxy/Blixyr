from Parser import *
from Lexer import *

class Interpreter:
    def __init__(self, nodes: list[Node]) -> None:
        self.nodes: list[Node] = nodes

        self.pos: int = -1
        self.current_node: Node = self.nodes[self.pos] if nodes else None

    def get_val(self, node: ValueNode, global_symbols) -> str:
        match node.type:
            case NodeType.VarAccNode:
                try:
                    return global_symbols[node.values[0]].values[0]
                except KeyError:
                    raise NameError(f'Identifier "{node.values[0]}" not found in the global namespace')
            
            case _:
                return node.values[0]

    def advance(self) -> None:
        self.pos += 1
        self.current_node = self.nodes[self.pos]

    def interpret(self, global_symbols) -> int:
        if not self.nodes:
            return 0

        while self.pos + 1 < len(self.nodes):
            self.advance()

            match self.current_node.type:
                case NodeType.PrintNode:
                    print(self.get_val(self.current_node.values[0], global_symbols), end='\n' if self.current_node.values[1] else '', flush=True)
 
                case NodeType.VarDecNode:
                    global_symbols[self.current_node.values[0]] = self.current_node.values[1]
                
                case NodeType.InputNode:
                    global_symbols[self.current_node.values[0]] = StringNode(input())

                case NodeType.GetchNode:
                    key =__import__('msvcrt').getch()

                    if self.current_node.values[0]:
                        global_symbols[self.current_node.values[0]] = BytesNode(key)

                case NodeType.StringConvertNode:
                    identifier = self.current_node.values[0]
                    match global_symbols[identifier].type:
                        case NodeType.BytesNode:
                            global_symbols[identifier] = StringNode(global_symbols[identifier].values[0].decode())
                        case NodeType.StringNode:
                            pass # It stays the same
                        case _:
                            raise SyntaxError(f'Conversion from type "{global_symbols[identifier].values[0].name}" to "string" is not supported.')

        return 0
