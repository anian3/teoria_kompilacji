#!/usr/bin/python
from enum import Enum, auto


class Type(Enum):
    INTNUM = auto()
    FLOAT = auto()
    STRING = auto()
    VECTOR = auto()
    MATRIX = auto()
    BOOLEAN = auto()
    RANGE = auto()
    NULL = auto()
    UNKNOWN = auto()


class Symbol:
    def __init__(self, name, mtype, matrix_size=None):
        self.name = name
        self.type = mtype
        self.matrix_size = matrix_size


class VariableSymbol(Symbol):
    def __init__(self, name, mtype,  matrix_size=None):
        super().__init__(name, mtype, matrix_size)


class FunctionDefinition(Symbol):
    def __init__(self, name, return_type, parameters):
        super().__init__(name, return_type)
        self.parameters = parameters


class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        elif self.parent:
            return self.parent.get(name)

    def check_exists(self, name):
        return self.get(name) is not None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        new_scope = SymbolTable(self, name)
        return new_scope

    def popScope(self):
        return self.parent