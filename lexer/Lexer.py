__import__('sys').path.append(__import__('os').path.dirname(__file__))
from Token import *

SYMBOLS = ['=', '+', '{', '}', ',', '(', ")"]
KEYWORDS = ['var', 'input', 'getch', 'to_string', 'to_bytes', 'func', 'import']

class Lexer:
    def __init__(self, line: str) -> None:
        self.line: str = line
        self.pos: int = 0
        self.current_char: str = self.line[self.pos]

    def advance(self) -> None:
        self.pos += 1
        self.current_char = self.line[self.pos]
    
    def generate_tokens(self) -> list[Token]:   
        try:
            return self.tokenize()
        except IndexError:
            raise SyntaxError("Error: EOL Character Missing")

    def tokenize_strlit(self, str_lit_type: str) -> Token:
        tok_val: str = ''
        while self.current_char != str_lit_type:
            if self.current_char == '\\': # Escape Character
                self.advance()
                if self.current_char == 'n':
                    tok_val += '\n'
                elif self.current_char == '\\':
                    tok_val += '\\'
                elif self.current_char in ['"', "'"]:
                    tok_val += self.current_char
                else:
                    raise SyntaxError(f'Invalid Escape "\\{self.current_char}"')
                
                self.advance()
            else:
                tok_val += self.current_char
                self.advance()

        self.advance()

        return Token(TokenType.Literal, tok_val)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        if not self.line or self.line == '\n':
            return []

        while self.pos + 1 < len(self.line):
            while self.current_char.isspace():
                self.advance()

            tok_val: str = ''

            if self.current_char == '#':
                return tokens
            
            elif self.current_char in ['\n', '\r']:
                self.advance()
                continue
            
            elif self.current_char in ["'", '"']:
                str_lit_type: str = self.current_char
                self.advance()

                tokens.append(self.tokenize_strlit(str_lit_type))

            elif self.current_char in SYMBOLS:
                tokens.append(Token(TokenType.Symbol, self.current_char))
                self.advance()

            elif self.current_char.isdigit():
                while self.current_char.isdigit():
                    tok_val += self.current_char
                    self.advance()

                tokens.append(Token(TokenType.Number, tok_val))

            elif self.current_char.isalpha() or self.current_char == '_':
                while self.current_char.isalnum() or self.current_char == '_':
                    tok_val += self.current_char
                    self.advance()

                is_keyword = tok_val in KEYWORDS

                is_bool = tok_val in ['true', 'false']

                tokens.append(Token(TokenType.Keyword if is_keyword else TokenType.Bool_Literal if is_bool else TokenType.Identifier, tok_val))

                if is_keyword and self.current_char == ' ':
                    self.advance()

            elif self.current_char == ';':
                tokens.append(Token(TokenType.EOL, 'EOL'))
                self.advance()

            else:
                raise SyntaxError(f"Illegal Character \"{self.current_char.encode()}\"")
        
        tokens.append(Token(TokenType.EOL, 'EOF'))

        return tokens
