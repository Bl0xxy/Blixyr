# Implemented Python Features into Blixyr
__import__('sys').path.append(__import__('os').path.dirname(__import__('os').path.dirname(__file__)))

from runtime.Interpreter import *

def func_exec() -> FuncNode:
    return FuncNode([PythonNode(VarAccNode('args'), True)])

def main() -> dict:
    return {'exec': func_exec()}