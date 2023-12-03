#!/usr/bin/python
import AST
from SymbolTable import SymbolTable, Type, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self):
        super().__init__()
        self.all_correct = True
        self.symbol_table = SymbolTable(None, "program")

    def printError(self, message):
        self.all_correct = False
        print(message)

    def visit_Program(self, node: AST.Program):
        for statement in node.statements:
            self.visit(statement)

    def visit_IntNum(self, node):
        return Type.INTNUM

    def visit_FloatNum(self, node):
        return Type.FLOAT

    def visit_String(self, node):
        return Type.STRING

    def visit_Variable(self, node):
        variable_name = node.value
        symbol = self.symbol_table.get(variable_name)
        if symbol:
            return symbol.type
        else:
            self.symbol_table.put(variable_name, VariableSymbol(variable_name, Type.UNKNOWN))
            return Type.UNKNOWN

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        if op in ['+', '-', '*', '/']:
            if type1 in [Type.INTNUM, Type.FLOAT] and type2 in [Type.INTNUM, Type.FLOAT]:
                return Type.FLOAT if Type.FLOAT in [type1, type2] else Type.INTNUM
            else:
                self.printError(f"Error in BinOp: wrong types {type1} {type2}.")
        elif op in ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV']:
            if type1 == Type.MATRIX and type2 == Type.MATRIX:
                if len(node.left) == len(node.right) and len(node.left[0]) == len(node.right[0]):
                    return Type.MATRIX
                else:
                    self.printError("Error in matrix BinOp: wrong matrix sizes")
            if type2 == Type.VECTOR and type2 == Type.VECTOR:
                if len(node.left) == len(node.right):
                    return Type.VECTOR
                else:
                    self.printError("Error in matrix BinOp: wrong vector sizes")
            else:
                self.printError(f"Error in matrix BinOp: wrong types {type1} {type2}.")
        else:
            self.printError("Erron in BinOp: wrong operand.")

    def visit_CompExpression(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if op in ['<', '>', 'MOREEQ', 'LESSEQ']:
            if type1 in [Type.INTNUM, Type.FLOAT] and type2 in [Type.INTNUM, Type.FLOAT]:
                return Type.BOOLEAN
            else:
                self.printError(f"Error in CompExpression: relational operations are not defined for types {type1} {type2}")
        elif op in ['NOTEQ', 'EQUAL']:
            if (type1 in [Type.INTNUM, Type.FLOAT] and type2 in [Type.INTNUM, Type.FLOAT]) or type1 == type2:
                return Type.BOOLEAN
            else:
                self.printError(f"Error in EQUAL / NOTEQ: not defined for types {type1} {type2}.")
        else:
            self.printError("Error in CompExpression: wrong operand")

    def visit_TransposeExpression(self, node):
        if node.value == Type.MATRIX and node.op == "'":
            return Type.MATRIX
        else:
            self.printError("Error in TransposeExpression.")

    def visit_UMinExpression(self, node):
        type = self.visit(node.value)
        if node.op == "-" and type in [Type.INTNUM, Type.FLOAT, Type.VECTOR, Type.MATRIX]:
            return type
        else:
            self.printError("Error in UMinExpression.")

    def visit_AssignExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        if node.left == AST.Variable and node.op == '=':
            self.symbol_table.put(node.left.value, VariableSymbol(node.left.value, type2))
            return type2
        elif node.op in ['ADDASIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN']:
            if node.left == AST.Variable and self.symbol_table.check_exists(node.left.value):
                if type1 in [Type.INTNUM, Type.FLOAT] and type2 in [Type.INTNUM, Type.FLOAT]:
                    return_type = Type.FLOAT if Type.FLOAT in [type1, type2] else Type.INTNUM
                    self.symbol_table.put(node.left.value, VariableSymbol(node.left.value, return_type))
                    return return_type
                else:
                    self.printError(f"Error in AssignExpr: operation not defined for types {type1} {type2}.")
            elif type1 in [Type.INTNUM, Type.FLOAT] and type2 in [Type.INTNUM, Type.FLOAT]:  # dla sytuacji 2 += 3
                    return Type.FLOAT if Type.FLOAT in [type1, type2] else Type.INTNUM
            else:
                self.printError("Error in AssignExpr: variable not defined.")

    def visit_MatrixInitFuncExpr(self, node):
        type = self.visit(node.size)
        if node.func in ['ZEROS', 'EYE', 'ONES'] and type == Type.INTNUM:
            return Type.MATRIX
        self.printError(f"Error in MatrixInitFuncExpr: can't use {node.func} with {type}.")

    def visit_MatrixRow(self, node):
        return Type.VECTOR

    def visit_MatrixInitWithValues(self, node):
        size = len(node.matrix_rows[0].value)
        for row in node.matrix_rows:
            if self.visit(row) != Type.VECTOR or len(row.value) != size:
                self.printError("Error in MatrixInitWithValues: wrong vector values.")
                return
        return Type.MATRIX

    def visit_IfExpr(self, node):
        self.visit(node.condition)
        self.visit(node.block)
        self.visit(node.ifx)

    def visit_ElseExpr(self, node):
        self.visit(node.block)

    def visit_RangeExpr(self, node):
        type1 = self.visit(node.startVal)
        type2 = self.visit(node.endVal)
        if type1 == Type.INTNUM and type2 == Type.INTNUM:
            return Type.RANGE
        self.printError("Error in RangeExpr: start and end must be int values.")

    def visit_ForLoopExpr(self, node):
        type1 = self.visit(node.range_expr)
        if node.loop_variable == AST.Variable and type1 == Type.RANGE:
            self.symbol_table = self.symbol_table.pushScope("for")
            self.symbol_table.put(node.loop_variable.value, VariableSymbol(node.loop_variable.value, Type.INTNUM)) # tylko pytanie czy w pętli można to modyfikować
            self.visit(node.body)
            self.symbol_table = self.symbol_table.popScope() # tylko zmienna stworzona w pętli powinna istnieć poza nią
            # self.symbol_table.symbols.pop(node.loop_variable.value)
        else:
            self.printError("Error in ForLoopExpr: error in range.")

    def visit_WhileLoopExpr(self, node):
        self.symbol_table = self.symbol_table.pushScope("while")
        self.visit(node.condition)
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()

    def visit_BreakExpr(self, node):
        if self.symbol_table.name not in ['while', 'for']:
            self.printError("BREAK outside loop.")

    def visit_ContinueExpr(self, node):
        if self.symbol_table.name not in ['while', 'for']:
            self.printError("CONTINUE outside loop.")

    def visit_ReturnExpr(self, node):
        pass

    def visit_PrintExpr(self, node):
        self.visit(node.val)

    def visit_IndexRef(self, node):
        if len(node.value) > 2:
            self.printError("Error in IndexRef: too many indices.")
            return
        for ind in node.value:
            if self.visit(ind) != Type.INTNUM:
                self.printError("Error in IndexRef: indices must be int values.")

    def visit_MatrixIndexRef(self, node):
        type1 = self.visit(node.matrix)
        self.visit(node.IndexRef)
        if (type1 == Type.MATRIX and len(node.IndexRef) == 2) or (type1 == Type.VECTOR and len(node.IndexRef) == 1):
            return Type.FLOAT # dla uproszczenia wszystkie macierze z floatami, można to zmienić
        self.printError("Error in MatrixIndexRef.")

