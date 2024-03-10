from enum import Enum

class TokenType(Enum):
    Identifier = 0
    Symbol = 1
    Literal = 2
    Keyword = 3
    EOL = 4
    Bool_Literal = 5
    Number = 6

class Token:
    def __init__(self, type: TokenType, value: str) -> None:
        self.type: TokenType = type
        self.value: str = value

    def __repr__(self) -> str:
        return f'Returned Token object with type "{self.type.name}" and value "{self.value}"'
    