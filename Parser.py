__import__('sys').path.append(__import__('os').path.dirname(__file__))
from Node import *
from Token import *

types = ['string', 'bytes']

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens: list[Token] = tokens
        self.pos: int = 0
        self.current_tok: Token = self.tokens[self.pos] if self.tokens else None
    
    def advance(self, amount: int = 1):
        self.pos += amount
        self.current_tok = self.tokens[self.pos]

    def parse_value(self) -> type:
        if self.current_tok.type == TokenType.Identifier:
            return VarAccNode
        elif self.current_tok.type == TokenType.Literal:
            return ValueNode
        elif self.current_tok.type == TokenType.Number:
            return NumberNode
        elif self.current_tok.type == TokenType.Bool_Literal:
            return BoolNode
        else:
            raise SyntaxError(f"Expected type identifier or literal, got {self.current_tok.type.name}")

    def parse_vardec(self) -> VarDecNode:
        self.advance()

        if self.current_tok.type != TokenType.Identifier:
            raise SyntaxError("Expected Identifier in variable declaration")
        
        identifier = self.current_tok.value

        self.advance()

        if not (self.current_tok.type == TokenType.Identifier or self.current_tok.value == '='):
            raise SyntaxError(f"Expected Symbol \"=\" after identifier in variable declaration, instead got {self.current_tok.type.name} \"{self.current_tok.value}\"")
        
        self.advance()

        return VarDecNode(identifier, self.parse_value()(self.current_tok.value))

    def parse_print(self) -> PrintNode:
        if self.tokens[self.pos + 1].type == TokenType.EOL:
            return PrintNode(StringNode(''))

        self.advance()

        if self.current_tok.type == TokenType.Identifier:
            val = VarAccNode(self.current_tok.value)
        else:
            val = StringNode(str(self.current_tok.value))

        if self.tokens[self.pos + 1].type == TokenType.EOL:
            return PrintNode(val)
        
        self.advance()

        if self.current_tok.type not in [TokenType.Bool_Literal, TokenType.Identifier]:
            raise SyntaxError(f"Expected bool or identifier as second argument for print, instead got {self.current_tok.type.name}")
        
        return PrintNode(val, self.parse_value()(self.current_tok.value == 'true'))

    def parse_getch(self) -> GetchNode:
        if self.tokens[self.pos + 1].type not in [TokenType.EOL, TokenType.Identifier]:
            raise SyntaxError(f"Expected EOL or Identifier, instead got {self.tokens[self.pos + 1].type.name}")
        
        return GetchNode(self.tokens[self.pos + 1].value)    

    def parse_varmod(self) -> VarModNode: # Special Call by Main Parser Method, First Checks Already Done
        identifier = self.current_tok.value

        self.advance(2)


        return VarModNode(identifier, self.parse_value()(self.current_tok.value))

    def parse_conversion(self) -> ConvertNode:
        if self.tokens[self.pos + 1].type != TokenType.Identifier:
            raise SyntaxError(f"Expected identifier to convert type, instead got {self.tokens[self.pos + 1].type.name}")
        
        match self.current_tok.value.lstrip('to_'):
            case 'string':
                self.advance()
                return StringConvertNode(self.current_tok.value)
            case 'bytes':
                self.advance()
                return BytesConvertNode(self.current_tok.value)
            case _:
                raise SyntaxError(f"Invalid Type \"{self.current_tok.value.lstrip('to_')}\"")
            
    def parse_input(self) -> InputNode:
        self.advance()

        if self.current_tok.type not in [TokenType.EOL, TokenType.Identifier]:
            raise SyntaxError("Expected EOL or Identifier after input keyword")
        
        return InputNode(self.current_tok.value)
    
    def parse_wait(self) -> WaitNode:
        self.advance()

        if self.current_tok.type not in [TokenType.Number, TokenType.Identifier]:
            raise SyntaxError("Expected Number or Identifier after wait keyword")
        
        if self.current_tok.type == TokenType.Identifier:
            val = VarAccNode(self.current_tok.value)

        elif self.current_tok.type == TokenType.Number:
            val = NumberNode(int(self.current_tok.value))
        
        return WaitNode(val)

    def parse_action(self) -> ActionNode:
        if self.current_tok.value == 'var':
            return self.parse_vardec()
        elif self.current_tok.value in ['print']:
            return self.parse_print()
        elif self.current_tok.value == 'getch':
            return self.parse_getch()
        elif self.current_tok.value in ['to_%s'%i for i in types]:
            return self.parse_conversion()
        elif self.current_tok.value == 'input':
            return self.parse_input()
        elif self.current_tok.value == 'wait':
            return self.parse_wait()
        else:
            raise SyntaxError(f"Invalid Keyword \"{self.current_tok.value}\"")

    def parse(self) -> list[Node]:
        if (not self.tokens) or self.tokens == []:
            return []

        if not any(token.type == TokenType.EOL for token in self.tokens):
            raise SyntaxError("Missing EOL Token")
        
        nodes: list[Node] = []

        while self.current_tok.type != TokenType.EOL:
            if self.current_tok.type == TokenType.Symbol:
                raise SyntaxError(f"Unexpected Token \"{self.current_tok.value}\"")
            
            elif self.current_tok.type == TokenType.Identifier:
                if self.tokens[self.pos + 1].value == '=' and self.tokens[self.pos + 1].type == TokenType.Symbol:
                    nodes.append(self.parse_varmod())
                else:
                    nodes.append(VarAccNode(self.current_tok.value))
                    self.advance()
                
                continue

            elif self.current_tok.type != TokenType.Keyword:
                self.advance()
                continue
            
            nodes.append(self.parse_action())
            
            self.advance()

        return nodes
