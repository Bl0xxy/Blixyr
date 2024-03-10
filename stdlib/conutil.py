# Console Utility Library for Blixyr
__import__('sys').path.append(__import__('os').path.dirname(__import__('os').path.dirname(__file__)))

from runtime.Interpreter import *

def func_clear():
    return FuncNode([PythonNode(StringNode('__import__("os").system("cls" if __import__("os").name == "nt" else "clear")'))])

def func_flush():
    return FuncNode([PythonNode(StringNode('__import__("sys").stdout.flush()'))])

def main() -> dict:
    return {'clear': func_clear(), 'flush': func_flush()}