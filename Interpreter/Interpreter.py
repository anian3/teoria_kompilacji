import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys
from operators import operators
import numpy as np

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Error)
    def visit(self, node):
        print(node.message)

    @when(AST.Program)
    def visit(self, node):
        for statement in node.statements:
            statement.accept(self)

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.memory. node.value

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        return operators[node.op](r1, r2)

    @when(AST.CompExpression)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)

        return operators[node.op](r1, r2)

    @when(AST.TransposeExpression)
    def visit(self, node):
        return node.value.T

    @when(AST.UMinExpression)
    def visit(self, node):
        return - node.value

    @when(AST.AssignExpr)
    def visit(self, node):
        key = node.left.accept(self)
        val = node.right.accept(self)
        if node.op == '=':
            self.memory.set(key, val)
            return
        if node.op == "ADDASSIGN":
            self.memory.set(key, self.memory.get(key) + val)
            return
        if node.op == "SUBASSIGN":
            self.memory.set(key, self.memory.get(key) - val)
            return
        if node.op == "MULASSIGN":
            self.memory.set(key, self.memory.get(key) * val)
            return
        if node.op == "DIVASSIGN":
            self.memory.set(key, self.memory.get(key) / val)

    @when(AST.MatrixInitFuncExpr)
    def visit(self, node):
        return operators[node.func](node.size)

    @when(AST.VectorValues)
    def visit(self, node):
        val = []
        for el in node.value:
            val.append(el.accept(self))
        return np.array(val)

    @when(AST.VectorInitWithValues)
    def visit(self, node):
        val = []
        for el in node.value:
            val.append(el.accept(self))
        return np.array(val)

    @when(AST.IfExpr)
    def visit(self, node):
        if node.condition.accept(self):
            for stmt in node.block:
                stmt.accept(self)
        else:
            node.ifx.accept(self)

    @when(AST.ElseExpr)
    def visit(self, node):
        for stmt in node.block:
            stmt.accept(self)

    @when(AST.RangeExpr)
    def visit(self, node):
        return [i for i in range(node.startVal.accept(self), node.endVal.accept(self))]

    @when(AST.ForLoopExpr)
    def visit(self, node):
        self.memory.push(Memory("ForLoop"))
        self.memory.insert(node.loop_variable, 0)
        for i in node.range_expr.accept(self):
            try:
                self.memory.set(node.loop_variable, i)
                for el in node.body:
                    el.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        return

    @when(AST.WhileLoopExpr)
    def visit(self, node):
        r = None
        while node.condition.accept(self):
            try:
                r = node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        return r

    @when(AST.BreakExpr)
    def visit(self, node):
        raise BreakException

    @when(AST.ContinueExpr)
    def visit(self, node):
        raise ContinueException

    @when(AST.ReturnExpr)
    def visit(self, node):
        return node.val

    @when(AST.PrintExpr)
    def visit(self, node):
        print(node.val)

    @when(AST.IndexRef)
    def visit(self, node):
        val = []
        for el in node.value:
            val.append(el)
        return val

    @when(AST.MatrixIndexRef)
    def visit(self, node):
        M = self.memory.get(node.matrix)
        I = node.indices.accept(self)
        if len(I) == 1:
            return M[I[0]]
        else:
            return M[I[0], I[1]]

