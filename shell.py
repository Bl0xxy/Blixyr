from Interpreter import *

global_symbols: dict = {}

def exec_line(line: str) -> int:
    global global_symbols

    try:
        lexer: Lexer = Lexer(line)
        tokens: list[Token] = lexer.generate_tokens()
    
    except Exception as e:
        print(f'LexingError: {e.args[0]}')
        return 1

    try:
        parser: Parser = Parser(tokens)
        nodes: list[Node] = parser.parse()

    except Exception as e:
        print(f'ParsingError: {e.args[0]}')
        return 1

    try:
        interpreter: Interpreter = Interpreter(nodes)

        res: int = interpreter.interpret(global_symbols)
    
    except Exception as e:
        print(f"InterpretingError: {e.args[0]}")
        return 1


    if res != 0:
        print("Fatal Error, Ending Proccess.  Please Report to the developers.  (Exit Code %s)"%str(res))
        raise SystemExit

    return 0

def run(fn: str):
    with open(fn) as f:
        lines = f.readlines()

    for line in lines:
        if exec_line(line) != 0:
            return

def main():
    print("Blixyr [v1.0]\n")
    while True:
        inp: str = input(">>> ")
        
        if not inp:
            continue

        if inp == 'exit':
            raise SystemExit
        elif inp.startswith('run '):
            run(inp)
        else:
            exec_line(inp)

if __name__ == '__main__':
    main()