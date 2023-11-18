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
class TransposeExpression(Node):
    """ Transpozycja macierzy i negacja unarna """
    op: Any
    value: Any


@dataclass
class UMinExpression(Node):
    """ Negacja unarna """
    op: Any
    value: Any


# INSTRUKCJE PRZYPISANIA
@dataclass
class AssignExpr(Node):
    op: Any
    left: Any
    right: Any


@dataclass
class MatrixInitFuncExpr(Node):
    func: Any
    size: int


# INSTRUKCJE WARUNKOWE IF-ELSE

# PĘTLE WHILE / FOR

class ForLoopExpr(Node):
    func = "FOR"
    

class WhileLoopExpr(Node):
    func = "WHILE"

# INSTRUKCJE: BREAK, CONTINUE, RETURN
@dataclass
class BreakExpr(Node):
    func = "BREAK"


@dataclass
class ContinueExpr(Node):
    func = "CONTINUE"


@dataclass
class ReturnExpr(Node):
    func = "RETURN"
    val: Any


# INSTRUKCJE: PRINT
@dataclass
class PrintExpr(Node):
    func = "PRINT"
    val: Any


# INSTRUKCJE ZŁOŻONE

# TABLICE ORAZ ICH ZAKRESY
@dataclass
class RangeExpr(Node):
    func = "RANGE"
    startVal: Any
    endVal: Any


# ERROR
class Error(Node):
    def __init__(self):
        pass
