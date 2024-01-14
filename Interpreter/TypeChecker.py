#!/usr/bin/python
import AST
from SymbolTable import SymbolTable, Type, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        if node is None:
            return
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
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
            elif type1 == Type.STRING and type2 == Type.INTNUM:
                return Type.STRING
            else:
                self.printError(f"Error in BinOp: wrong types {type1} {type2}.")
        elif op in ['.+', '.-', '.*', './']:
            sizes = [None, None]
            types = (type1, type2)
            for i, node_ in enumerate((node.left, node.right)):
                if type(node_) == AST.Variable:
                    sizes[i] = self.symbol_table.get(node_.value).matrix_size
                elif type(node_) == AST.VectorInitWithValues:
                    if types[i] == Type.VECTOR:
                        sizes[i] = len(node_.matrix_rows)
                    else:
                        sizes[i] = (len(node_.matrix_rows), len(node_.matrix_rows[0].matrix_rows))
                else:  # func
                   sizes[i] = node_.size
            if sizes[0] != sizes[1]:
                self.printError(f"Error in matrix BinOp: wrong sizes {sizes[0]}, {sizes[1]}.")
            else:
                if type1 == Type.MATRIX and type2 == Type.MATRIX:
                    return Type.MATRIX
                if type2 == Type.VECTOR and type2 == Type.VECTOR:
                    return Type.VECTOR
                else:
                    self.printError(f"Error in matrix BinOp: wrong types {type1} {type2} for op {op}.")
        else:
            self.printError(f"Error in BinOp: wrong operand {op}.")

    def visit_CompExpression(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        if op in ['<', '>', '>=', '<=']:
            if type1 in [Type.INTNUM, Type.FLOAT] and type2 in [Type.INTNUM, Type.FLOAT]:
                return Type.BOOLEAN
            else:
                self.printError(
                    f"Error in CompExpression: relational operations are not defined for types {type1} {type2}")
        elif op in ['!=', '==']:
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

        if type(node.left) == AST.Variable and node.op == '=':
            if type2 == Type.VECTOR or type2 == Type.MATRIX:  # dla macierzy, do zapisania ich rozmiaru w zmiennej
                if type(node.right) == AST.MatrixInitFuncExpr:
                    self.symbol_table.put(node.left.value, VariableSymbol(node.left.value, type2, node.right.size))
                elif type(node.right) == AST.BinExpr:
                    size = self.symbol_table.get(
                        node.right.left.value).matrix_size  # podstawiam rozmiar pierwszego elementu z binExpr
                    self.symbol_table.put(node.left.value, VariableSymbol(node.left.value, type2, size))
                elif type(node.right) == AST.VectorInitWithValues:
                    if type2 == Type.VECTOR:
                        self.symbol_table.put(node.left.value,
                                              VariableSymbol(node.left.value, type2, len(node.right.matrix_rows)))
                    else:
                        self.symbol_table.put(node.left.value,
                                              VariableSymbol(node.left.value, type2, [len(node.right.matrix_rows),
                                                                                      len(node.right.matrix_rows[
                                                                                              0].matrix_rows)]))
                else:
                    self.printError(f"Can't initialize matrix or vector using {type(node.right)}.")
            else:
                self.symbol_table.put(node.left.value, VariableSymbol(node.left.value, type2))
            return type2
        elif node.op in ['ADDASIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN']:
            if type(node.left) == AST.Variable and self.symbol_table.check_exists(node.left.value):
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
        if node.func in ['zeros', 'eye', 'ones'] and type == Type.INTNUM:
            if len(node.size.value) > 1:
                return Type.MATRIX
            else:
                return Type.VECTOR
        self.printError(f"Error in MatrixInitFuncExpr: can't use {node.func} with {type}.")

    def visit_VectorValues(self, node):
        return Type.VECTOR

    def visit_VectorInitWithValues(self, node):
        matrix = (self.visit(node.matrix_rows[0]) == Type.VECTOR)
        if matrix:
            size = len(node.matrix_rows[0].matrix_rows)
            for row in node.matrix_rows:
                if self.visit(row) != Type.VECTOR:
                    self.printError("Error in MatrixInitWithValues: wrong type")
                    return
                if len(row.matrix_rows) != size:
                    self.printError("Error in MatrixInitWithValues: different row lengths")
                    return
            return Type.MATRIX
        return Type.VECTOR

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
        self.printError("Error in RangeExr: start and end must be int values.")

    def visit_ForLoopExpr(self, node):
        type1 = self.visit(node.range_expr)
        if type(node.loop_variable) == AST.Variable and type1 == Type.RANGE:
            self.symbol_table = self.symbol_table.pushScope("for")
            self.symbol_table.put(node.loop_variable.value, VariableSymbol(node.loop_variable.value,
                                                                           Type.INTNUM))  # tylko pytanie czy w pętli można to modyfikować
            self.visit(node.body)
            self.symbol_table = self.symbol_table.popScope()  # tylko zmienna stworzona w pętli powinna istnieć poza nią
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
            if self.visit(ind) != Type.INTNUM and self.visit(ind) != Type.RANGE:
                self.printError("Error in IndexRef: indices must be int values.")
        return Type.INTNUM

    def visit_MatrixIndexRef(self, node):
        type1 = self.visit(node.matrix)
        self.visit(node.indices)
        if (type1 == Type.MATRIX and len(node.indices.value) == 2) or (
                type1 == Type.VECTOR and len(node.indices.value) == 1):
            return Type.FLOAT  # dla uproszczenia wszystkie macierze z floatami, można to zmienić
        self.printError("Error in MatrixIndexRef.")
