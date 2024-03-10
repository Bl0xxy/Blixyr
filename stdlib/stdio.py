# Standard IO Library for Blixyr
__import__('sys').path.append(__import__('os').path.dirname(__import__('os').path.dirname(__file__)))

from runtime.Interpreter import *

def func_print() -> FuncNode:
    return FuncNode([PrintNode(VarAccNode('args'))])

def func_println() -> FuncNode:
    return FuncNode([PrintNode(VarAccNode('args')), PrintNode(StringNode('\n'))])

def main() -> dict:
    return {'print': func_print(), 'println': func_println()}