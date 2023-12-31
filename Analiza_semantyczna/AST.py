from dataclasses import dataclass
from typing import Any, List


class Node(object):
    pass


@dataclass
class Program(Node):
    statements: List[Any]


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
    value: str


# WYRAŻENIA BINARNE
@dataclass
class BinExpr(Node):
    """ Wyrażenia binarne """
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
    """ Transpozycja macierzy """
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
    size: Any


@dataclass
class MatrixRow(Node):
    value: List[Any]


@dataclass
class MatrixInitWithValues(Node):
    matrix_rows: List[MatrixRow]


# INSTRUKCJE WARUNKOWE IF-ELSE
@dataclass
class IfExpr(Node):
    # func = "IF"
    condition: Any
    block: Any
    ifx: Any


@dataclass
class ElseExpr(Node):
    # func: str
    block: Any


# PĘTLE WHILE / FOR
@dataclass
class RangeExpr(Node):
    # func = "RANGE"
    startVal: Node
    endVal: Any


@dataclass
class ForLoopExpr(Node):
    # func = "FOR"
    loop_variable: Any
    range_expr: RangeExpr
    body: Any


@dataclass
class WhileLoopExpr(Node):
    # func = "WHILE"
    condition: Any
    body: Any


# INSTRUKCJE: BREAK, CONTINUE, RETURN
@dataclass
class BreakExpr(Node):
    # func = "BREAK"
    pass


@dataclass
class ContinueExpr(Node):
    # func = "CONTINUE"
    pass


@dataclass
class ReturnExpr(Node):
    # func = "RETURN"
    val: Any


# INSTRUKCJE: PRINT
@dataclass
class PrintExpr(Node):
    # func = "PRINT"
    val: Any


# TABLICE ORAZ ICH ZAKRESY

@dataclass
class IndexRef(Node):
    value: List[Any]


@dataclass
class MatrixIndexRef(Node):
    matrix: Any
    indices: IndexRef


# ERROR
@dataclass
class Error(Node):
    message: str

