# Implemented Python Features into Blixyr
__import__('sys').path.append(__import__('os').path.dirname(__import__('os').path.dirname(__file__)))

from runtime.Interpreter import *

def func_wait() -> FuncNode:
    return FuncNode([WaitNode(VarAccNode('args'))])

def main() -> dict:
    return {'wait': func_wait()}