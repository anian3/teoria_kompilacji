from dataclasses import dataclass
from typing import Any, List


class Node(object):
    def accept(self, visitor):
        return visitor.visit(self)

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
    line_number: int


# WYRAŻENIA RELACYJNE
@dataclass
class CompExpression(Node):
    op: Any
    left: Any
    right: Any
    line_number: int


@dataclass
class TransposeExpression(Node):
    """ Transpozycja macierzy """
    op: Any
    value: Any
    line_number: int


@dataclass
class UMinExpression(Node):
    """ Negacja unarna """
    op: Any
    value: Any
    line_number: int


# INSTRUKCJE PRZYPISANIA
@dataclass
class AssignExpr(Node):
    op: Any
    left: Any
    right: Any
    line_number: int


@dataclass
class MatrixInitFuncExpr(Node):
    func: Any
    size: Any
    line_number: int


@dataclass
class VectorValues(Node):
    value: List[Any]
    line_number: int


@dataclass
class VectorInitWithValues(Node):
    matrix_rows: List[VectorValues]
    line_number: int


# INSTRUKCJE WARUNKOWE IF-ELSE
@dataclass
class IfExpr(Node):
    condition: Any
    block: Any
    ifx: Any
    line_number: int


@dataclass
class ElseExpr(Node):
    block: Any
    line_number: int


# PĘTLE WHILE / FOR
@dataclass
class RangeExpr(Node):
    startVal: Node
    endVal: Any
    line_number: int


@dataclass
class ForLoopExpr(Node):
    loop_variable: Any
    range_expr: RangeExpr
    body: Any
    line_number: int


@dataclass
class WhileLoopExpr(Node):
    condition: Any
    body: Any
    line_number: int


# INSTRUKCJE: BREAK, CONTINUE, RETURN
@dataclass
class BreakExpr(Node):
    pass


@dataclass
class ContinueExpr(Node):
    pass


@dataclass
class ReturnExpr(Node):
    val: Any
    line_number: int


# INSTRUKCJE: PRINT, RETURN
@dataclass
class PrintExpr(Node):
    val: Any
    line_number: int


# ZAKRES

@dataclass
class IndexRef(Node):
    value: List[Any]
    line_number: int


@dataclass
class MatrixIndexRef(Node):
    matrix: Any
    indices: IndexRef
    line_number: int

