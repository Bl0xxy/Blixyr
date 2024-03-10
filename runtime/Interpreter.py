from os import path

__import__('sys').path.append(path.dirname(path.dirname(__file__)))
__import__('sys').path.append(path.join(path.dirname(path.dirname(__file__)), 'stdlib'))
from parser.Parser import *
from lexer.Lexer import *

class Interpreter:
    def __init__(self, nodes: list[Node]) -> None:
        self.nodes: list[Node] = nodes

        self.pos: int = -1
        self.current_node: Node = self.nodes[self.pos] if self.nodes else None

    def advance(self, amount: int = 1) -> None:
        self.pos += amount
        self.current_node = self.nodes[self.pos]

    def interpret_value(self, node: ValueNode, global_symbols) -> str:
        if node.type == NodeType.VarAccNode:
            try:
                child = global_symbols[node.children[0]].children[0]

                if isinstance(child, list):
                    if not child:
                        return ''
                    if len(child) == 1:
                        return self.interpret_value(child[0], global_symbols)
                    return [ch for ch in child]
                
                return child
            except KeyError:
                raise NameError(f'Identifier "{node.children[0]} not found in the global namespace"')

        return node.children[0]

    def interpret(self, global_symbols) -> int:
        if not self.nodes:
            return 0
        
        while self.pos + 1 < len(self.nodes):
            self.advance()

            match self.current_node.type:
                case NodeType.PrintNode:
                    print(str(self.interpret_value(self.current_node.children[0], global_symbols)), end='', flush=self.current_node.children[1].children[0])
                
                case NodeType.VarDecNode:
                    value: str = self.interpret_value(self.current_node.children[1], global_symbols)

                    if self.current_node.children[0] in global_symbols:
                        raise SyntaxError(f'Variable {self.current_node.children[0]} is already declared in the global namespace.')

                    global_symbols[self.current_node.children[0]] = ValueNode(value, self.current_node.children[1].type)

                case NodeType.InputNode:
                    global_symbols[self.current_node.children[0]] = StringNode(input())

                case NodeType.GetchNode:
                    key: bytes = __import__('msvcrt').getch()

                    if self.current_node.children and self.current_node.children[0]:
                        global_symbols[self.current_node.children[0]] = BytesNode(key)

                case NodeType.StringConvertNode:
                    identifier: str = self.current_node.children[0]
                    old_val: ValueNode = global_symbols[identifier]

                    if old_val.type == NodeType.BytesNode:
                        global_symbols[identifier] = StringNode(old_val.children[0].decode())
                    elif old_val.type == NodeType.StringNode:
                        pass
                    else:
                        raise SyntaxError(f'Conversion from type "{old_val.type.name}" to "string" is not supported.')
                    
                case NodeType.BytesConvertNode:
                    identifier: str = self.current_node.children[0]
                    old_val: ValueNode = global_symbols[identifier]

                    if old_val.type == NodeType.StringNode:
                        global_symbols[identifier] = BytesNode(old_val.children[0].encode())
                    elif old_val.type == NodeType.BytesNode:
                        pass
                    else:
                        raise SyntaxError(f'Conversion from type "{old_val.type.name}" to "bytes" is not supported.')
                    
                case NodeType.VarAccNode:
                    identifier: str = self.current_node.children[0]
                    
                    if identifier not in global_symbols:
                        raise SyntaxError(f'Identifier "{identifier}" not found in the global namespace.')

                case NodeType.VarModNode:
                    identifier: str = self.current_node.children[0]
                    value: str = self.interpret_value(self.current_node.children[1], global_symbols)

                    if identifier not in global_symbols:
                        raise SyntaxError(f'Identifier "{identifier}" not found in the global namespace.')
                    
                    global_symbols[identifier] = ValueNode(value, global_symbols[identifier].type)

                case NodeType.WaitNode:
                    __import__('time').sleep(int(self.interpret_value(self.current_node.children[0], global_symbols)))

                case NodeType.FuncCallNode:
                    identifier = self.current_node.children[0]
                    args = self.current_node.children[1]

                    if identifier not in global_symbols:
                        raise SyntaxError(f'Identifier "{identifier}" not found in the global namespace.')
                    scope = global_symbols.copy()
                    scope.update({'args': ListNode(args)})

                    Interpreter(global_symbols[identifier].children[0]).interpret(scope)

                case NodeType.PythonNode:
                    line = self.interpret_value(self.current_node.children[0], global_symbols)

                    if self.current_node.children[1]:
                        args = (line, {})
                    else:
                        args = tuple([line])
                    try:
                        exec(*args)
                    except Exception as e:
                        print("Python Error: %s"%repr(e))

                case NodeType.ImportNode:
                    global_symbols.update(__import__(self.current_node.children[0]).main())
                          
                case _:
                    raise SyntaxError(f"error.internal.invalid_node_type; TYPE: {self.current_node.type}")
                
        return 0
    
