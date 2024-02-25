from Node import *
from Token import *

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.pos: int = 0
        self.current_tok: Token = self.tokens[self.pos] if tokens else None

    def advance(self, amount: int = 1):
        self.pos += amount
        self.current_tok = self.tokens[self.pos]
    
    def has_eol(self):
        for token in self.tokens:
            if token.type == TokenType.EOL:
                return 1
        
        return 0
    
    def parse_print(self, newline: bool) -> PrintNode:
        self.advance()

        match self.current_tok.type:
            case TokenType.Identifier:
                val_tok: StringNode = VarAccNode(self.current_tok.value)
            case TokenType.Literal:
                val_tok: StringNode = ValueNode(self.current_tok.value)
            case _:
                raise SyntaxError(f'Invalid token "{self.current_tok.type.name}" in "PrintNode"')

        return PrintNode(val_tok, newline)

    def parse_vardec(self) -> VarDecNode:
        self.advance()

        if self.current_tok.type != TokenType.Identifier:
            raise SyntaxError("Expected Identifier after keyword \"var\"")
        
        identifier = self.current_tok.value

        self.advance()

        if self.current_tok.value != '=':
            raise SyntaxError("Expected Symbol \"=\" after identifier in variable declaration")
        
        self.advance()

        match self.current_tok.type:
            case TokenType.Identifier:
                val = VarAccNode(self.current_tok.value)
            
            case TokenType.Literal:
                val = ValueNode(self.current_tok.value)

            case _:
                raise SyntaxError("Expected Literal or Identifier to assign to \"%s\""%identifier)
            
        return VarDecNode(identifier, val)
    
    def parse_input(self) -> InputNode:
        self.advance()

        if self.current_tok.type != TokenType.Identifier:
            raise SyntaxError("Expected Identifier to Assign Input Value to")
        
        return InputNode(self.current_tok.value)
    
    def parse_getch(self) -> GetchNode:
        self.advance()

        if self.current_tok.type == TokenType.EOL:
            self.advance(-1)
            return GetchNode('')
        elif self.current_tok.type == TokenType.Identifier:
            return GetchNode(self.current_tok.value)
        else:
            raise SyntaxError("Expected EOL or Identifier After \"getch\" Keyword")
        
    def parse_to_str(self) -> StringConvertNode:
        self.advance()

        if self.current_tok.type != TokenType.Identifier:
            raise SyntaxError("Expected Identifier after \"str\" Keyword")
        
        return StringConvertNode(self.current_tok.value)

    def parse(self) -> list[Node]:
        nodes: list[Node] = []

        if not self.tokens:
            return []

        if not self.has_eol():
            raise SyntaxError("Missing EOL Token")

        while self.current_tok.type != TokenType.EOL:
            if self.current_tok.type == TokenType.Keyword:
                if self.current_tok.value == "var":
                    nodes.append(self.parse_vardec())
                    self.advance()
                    continue

                elif self.current_tok.value in ['print', 'println']:
                    newline: bool = self.current_tok.value == 'println'
                    self.advance()
                    if self.current_tok.type == TokenType.EOL:
                        nodes.append(PrintNode(StringNode(''), newline))
                        self.advance(-1)
                    else:
                        self.advance(-1)
                        nodes.append(self.parse_print(newline))

                    self.advance()
                    continue

                elif self.current_tok.value == 'input':
                    nodes.append(self.parse_input())
                    self.advance()
                    continue

                elif self.current_tok.value == 'getch':
                    nodes.append(self.parse_getch())
                    self.advance()
                    continue

                elif self.current_tok.value == 'to_str':
                    nodes.append(self.parse_to_str())
                    self.advance()
                    continue

            else:
                raise SyntaxError("Invalid Token")

        return nodes
