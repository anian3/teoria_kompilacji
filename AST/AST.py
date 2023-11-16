from dataclasses import dataclass
from typing import Any

class Node(object):
    pass

# ZMIENNE

@dataclass
class IntNum(Node):
    """ Integer variable type """
    value: int

@dataclass
class FloatNum(Node):
    """ Float variable type """
    value: float


@dataclass
class String(Node):
    """ String variable type """
    value: str


@dataclass
class Variable(Node):
    """ ID """
    name: Any
    value: Any


# WYRAŻENIA BINARNE
@dataclass
class BinExpr(Node):
    """ Wyrażenia binarne """
    op: Any
    left: Any
    right: Any


@dataclass
class MatExpr(Node):
    """ Operacje macierzowe """
    op: Any
    left: Any
    right: Any


# WYRAŻENIA RELACYJNE
@dataclass
class CompExpression(Node):
    op: Any
    left: Any
    right: Any


@dataclass
class OneExpression(Node):
    """ Jednoelementowe wyrażenia: transpozycja macierzy i negacja unarna """
    op: Any
    value: Any


 # INSTRUKCJE PRZYPISANIA
@dataclass
class AssignExpr(Node):
    op: Any
    left: Any
    right: Any


# INSTRUKCJE WARUNKOWE IF-ELSE

# PĘTLE WHILE / FOR

# INSTRUKCJE: BREAK, CONTINUE, RETURN

# INSTRUKCJE: PRINT

# INSTRUKCJE ZŁOŻONE

# TABLICE ORAZ ICH ZAKRESY


# ERROR
class Error(Node):
    def __init__(self):
        pass
      
