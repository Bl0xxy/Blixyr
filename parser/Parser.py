__import__('sys').path.append(__import__('os').path.dirname(__file__))
__import__('sys').path.append(__import__('os').path.dirname(__import__('os').path.dirname(__file__)))
from Node import *
from lexer.Token import *

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
        if self.current_tok.type.value == TokenType.Identifier.value:
            return VarAccNode
        elif self.current_tok.type.value == TokenType.Literal.value:
            return ValueNode
        elif self.current_tok.type.value == TokenType.Number.value:
            return NumberNode
        elif self.current_tok.type.value == TokenType.Bool_Literal.value:
            return BoolNode
        else:
            raise SyntaxError(f"Expected type identifier or literal, got {self.current_tok.type.name}")

    def parse_vardec(self) -> VarDecNode:
        self.advance()

        if self.current_tok.type.value != TokenType.Identifier.value:
            raise SyntaxError(f"Expected Identifier in variable declaration, instead got {self.current_tok.type.name}")
        
        identifier = self.current_tok.value

        self.advance()

        if not (self.current_tok.type.value == TokenType.Identifier.value or self.current_tok.value == '='):
            raise SyntaxError(f"Expected Symbol \"=\" after identifier in variable declaration, instead got {self.current_tok.type.name} \"{self.current_tok.value}\"")
        
        self.advance()

        return VarDecNode(identifier, self.parse_value()(self.current_tok.value))

    def parse_getch(self) -> GetchNode:
        if self.tokens[self.pos + 1].type.value not in [TokenType.EOL.value, TokenType.Identifier.value]:
            raise SyntaxError(f"Expected EOL or Identifier, instead got {self.tokens[self.pos + 1].type.name}")
        
        return GetchNode(self.tokens[self.pos + 1].value)    

    def parse_varmod(self) -> VarModNode: # Special Call by Main Parser Method, First Checks Already Done
        identifier = self.current_tok.value

        self.advance(2)


        return VarModNode(identifier, self.parse_value()(self.current_tok.value))

    def parse_conversion(self) -> ConvertNode:
        if self.tokens[self.pos + 1].type.value != TokenType.Identifier.value:
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

        if self.current_tok.type.value not in [TokenType.EOL.value, TokenType.Identifier.value]:
            raise SyntaxError("Expected EOL or Identifier after input keyword")
        
        return InputNode(self.current_tok.value)

    def parse_func(self) -> VarDecNode:
        self.advance()

        if self.current_tok.type.value != TokenType.Identifier.value:
            raise SyntaxError("Expected Identifier in Function Declaration, instead got " + self.current_tok.type.name)
        
        identifier = self.current_tok.value

        self.advance()

        if not (self.current_tok.type.value == TokenType.Symbol.value and self.current_tok.value == '('):
            raise SyntaxError("Expected Symbol \"(\" after identifier")
        
        self.advance()

        while not (self.current_tok.value == ')' and self.current_tok.type.value == TokenType.Symbol.value):
            self.advance()
        
        self.advance()

        if not (self.current_tok.type.value == TokenType.Symbol.value and self.current_tok.value == '{'):
            raise SyntaxError("Expected Symbol \"{\", instead got \"" + self.current_tok.value + "\".")
        
        toks: list[Token] = []

        while not (self.current_tok.value == '}' and self.current_tok.type.value == TokenType.Symbol.value):
            self.advance()
            toks.append(self.current_tok)

        toks[-1] = Token(TokenType.EOL, 'EOF')

        return VarDecNode(identifier, FuncNode(Parser(toks).parse()))
    
    def parse_func_call(self) -> FuncCallNode:
        identifier = self.current_tok.value

        self.advance(2)

        args: list[ValueNode] = []

        while not (self.current_tok.value == ')' and self.current_tok.type.value == TokenType.Symbol.value):
            if (self.current_tok.type.value == TokenType.Symbol.value and self.current_tok.value == ','):
                self.advance()
                continue
            args.append(self.parse_value()(self.current_tok.value))
            self.advance()

        self.advance()

        return FuncCallNode(identifier, args)

    def parse_import(self) -> ImportNode:
        self.advance()

        if self.current_tok.type.value != TokenType.Identifier.value:
            raise SyntaxError("Expected module name to import")
        
        module: str = self.current_tok.value

        return ImportNode(module)

    def parse_action(self) -> ActionNode:
        if self.current_tok.value == 'var':
            return self.parse_vardec()
        elif self.current_tok.value == 'getch':
            return self.parse_getch()
        elif self.current_tok.value in ['to_%s'%i for i in types]:
            return self.parse_conversion()
        elif self.current_tok.value == 'input':
            return self.parse_input()
        elif self.current_tok.value == 'func':
            return self.parse_func()
        elif self.current_tok.value == 'import':
            return self.parse_import()
        else:
            raise SyntaxError(f"Invalid Keyword \"{self.current_tok.value}\"")

    def parse(self) -> list[Node]:
        if (not self.tokens) or self.tokens == []:
            return []
        
        if not (any(token.type.value == TokenType.EOL.value for token in self.tokens) and any(token.value == 'EOF' for token in self.tokens)):
            raise SyntaxError("Missing EOL Token")
        
        nodes: list[Node] = []

        while not (self.current_tok.type.value == TokenType.EOL.value and self.current_tok.value == 'EOF'):
            if self.current_tok.type.value == TokenType.Symbol.value:
                raise SyntaxError(f"Unexpected Token \"{self.current_tok.value}\"")
            
            elif self.current_tok.type.value == TokenType.Identifier.value:
                if self.tokens[self.pos + 1].value == '=' and self.tokens[self.pos + 1].type.value == TokenType.Symbol.value:
                    nodes.append(self.parse_varmod())
                elif self.tokens[self.pos + 1].value == '(' and self.tokens[self.pos + 1].type.value == TokenType.Symbol.value:
                    nodes.append(self.parse_func_call())
                else:
                    nodes.append(VarAccNode(self.current_tok.value))
                    self.advance()
                
                continue

            elif self.current_tok.type.value != TokenType.Keyword.value:
                self.advance()
                continue 

            nodes.append(self.parse_action())
            
            self.advance()

        return nodes
