#!/usr/bin/python
import AST
from SymbolTable import SymbolTable, Type


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
        pass

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
                self.printError("Error in BinOp: wrong types")
        elif op in ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV']:
            if type1 == Type.MATRIX and type2 == Type.MATRIX:
                if node.left.size() == node.right.size() and node.left[0].size() == node.right[0].size():
                    return Type.MATRIX
                else:
                    self.printError("Error in matrix BinOp: wrong matrix sizes")
            if type2 == Type.VECTOR and type2 == Type.VECTOR:
                if node.left.size() == node.right.size():
                    return Type.VECTOR
                else:
                    self.printError("Error in matrix BinOp: wrong vector sizes")
            else:
                self.printError("Error in matrix BinOp: wrong types")
        else:
            self.printError("Erron in BinOp: wrong operands")


