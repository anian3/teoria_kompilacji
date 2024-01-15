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
        return int(node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return str(node.value)

    @when(AST.Variable)
    def visit(self, node):
        return self.memory.get(node.value)

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
        node.left.accept(self)
        val = node.right.accept(self)
        if isinstance(node.left, AST.Variable):
            key = node.left.value
            if node.op == '=':
                self.memory.insert(key, val)
                return
            if node.op == "+=":
                self.memory.set(key, self.memory.get(key) + val)
                return
            if node.op == "-=":
                self.memory.set(key, self.memory.get(key) - val)
                return
            if node.op == "*=":
                self.memory.set(key, self.memory.get(key) * val)
                return
            if node.op == "/=":
                self.memory.set(key, self.memory.get(key) / val)
        else:
            key = node.left.matrix.value
            M = self.memory.get(key)
            indices = node.left.indices.accept(self)
            if len(indices) == 1:
                prev_value = M[indices[0].value]
            else:
                prev_value = M[indices[0].value, indices[1].value]
            if node.op == '=':
                val_to_insert = val
            if node.op == "+=":
                val_to_insert = prev_value + val
            if node.op == "-=":
                val_to_insert = prev_value - val
            if node.op == "*=":
                val_to_insert = prev_value * val
            if node.op == "/=":
                val_to_insert = prev_value / val
            if len(indices) == 1:
                M[indices[0].value] = val_to_insert
            else:
                M[indices[0].value, indices[1].value] = val_to_insert


    @when(AST.MatrixInitFuncExpr)
    def visit(self, node):
        s = node.size.accept(self)
        if len(s) == 1:
            return operators[node.func](s[0].value)
        else:
            return operators[node.func](s[0].value, s[1].value)

    @when(AST.VectorValues)
    def visit(self, node):
        val = []
        for el in node.value:
            val.append(el.accept(self))
        return np.array(val)

    @when(AST.VectorInitWithValues)
    def visit(self, node):
        val = []
        for el in node.matrix_rows:
            val.append(el.accept(self))
        return np.array(val)

    @when(AST.IfExpr)
    def visit(self, node):
        if node.condition.accept(self):
            for stmt in node.block:
                stmt.accept(self)
        else:
            if node.ifx is not None:
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
        for i in node.range_expr.accept(self):
            self.memory.push(Memory("ForLoop"))
            self.memory.insert(node.loop_variable.value, i)
            try:
                if type(node.body) == list:
                    for el in node.body:
                        el.accept(self)
                else:
                    node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory.pop()
        return

    @when(AST.WhileLoopExpr)
    def visit(self, node):
        while node.condition.accept(self):
            self.memory.push(Memory("WhileLoop"))
            try:
                if type(node.body) == list:
                    for el in node.body:
                        el.accept(self)
                else:
                    node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                continue
        self.memory.pop()
        return

    @when(AST.BreakExpr)
    def visit(self, node):
        self.memory.pop()
        raise BreakException

    @when(AST.ContinueExpr)
    def visit(self, node):
        raise ContinueException

    @when(AST.ReturnExpr)
    def visit(self, node):
        return node.val

    @when(AST.PrintExpr)
    def visit(self, node):
        for val in node.val:
            print(val.accept(self))

    @when(AST.IndexRef)
    def visit(self, node):
        val = []
        for el in node.value:
            val.append(el)
        return val

    @when(AST.MatrixIndexRef)
    def visit(self, node):
        M = self.memory.get(node.matrix.value)
        I = node.indices.accept(self)
        if len(I) == 1:
            return M[I[0].value]
        else:
            return M[I[0].value, I[1].value]
