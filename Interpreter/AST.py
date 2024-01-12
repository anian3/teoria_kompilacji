from dataclasses import dataclass
from typing import Any, List


class Node(object):
    pass

# BŁĄD
@dataclass
class Error(Node):
    message: str

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
class VectorValues(Node):
    value: List[Any]


@dataclass
class VectorInitWithValues(Node):
    matrix_rows: List[VectorValues]


# INSTRUKCJE WARUNKOWE IF-ELSE
@dataclass
class IfExpr(Node):
    condition: Any
    block: Any
    ifx: Any


@dataclass
class ElseExpr(Node):
    block: Any


# PĘTLE WHILE / FOR
@dataclass
class RangeExpr(Node):
    # func = "RANGE"
    startVal: Node
    endVal: Any


@dataclass
class ForLoopExpr(Node):
    loop_variable: Any
    range_expr: RangeExpr
    body: Any


@dataclass
class WhileLoopExpr(Node):
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


# INSTRUKCJE: PRINT, RETURN
@dataclass
class PrintExpr(Node):
    val: Any


# ZAKRES

@dataclass
class IndexRef(Node):
    value: List[Any]


@dataclass
class MatrixIndexRef(Node):
    matrix: Any
    indices: IndexRef

