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
    def __init__(self, name, mtype):
        self.name = name
        self.type = mtype


class VariableSymbol(Symbol):
    def __init__(self, name, mtype):
        super().__init__(name, mtype)


class FunctionDefinition(Symbol):
    def __init__(self, name, return_type, parameters):
        super().__init__(name, return_type)
        self.parameters = parameters


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        symbol = self.symbols.get(name)
        if symbol:
            return symbol
        elif self.parent:
            return self.parent.get(name)

    def check_exists(self, name):
        return self.get(name) is not None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):  # add a new scope with this one as parent
        new_scope = SymbolTable(self, name)
        return new_scope

    def popScope(self):
        return self.parent