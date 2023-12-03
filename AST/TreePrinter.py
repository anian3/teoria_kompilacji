from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        for statement in self.statements:
            statement.printTree(indent)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    # ZMIENNE
    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("  " * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("  " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("  " * indent + str(self.value))

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("  " * indent + self.value)

    # Wyrażenia binarne i relacyjne
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.op))
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.CompExpression)
    def printTree(self, indent=0):
        print("  " * indent + str(self.op))
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    # Transpozycja i negacja unarna
    @addToClass(AST.TransposeExpression)
    def printTree(self, indent=0):
        print("  " * indent + "TRANSPOSE")
        self.value.printTree(indent + 1)

    @addToClass(AST.UMinExpression)
    def printTree(self, indent=0):
        print("  " * indent + "-")
        self.value.printTree(indent + 1)

    # Wyrażenia przypisania
    @addToClass(AST.AssignExpr)
    def printTree(self, indent=0):
        print("  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatrixInitFuncExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.func))
        self.size.printTree(indent + 1)

    @addToClass(AST.MatrixInitWithValues)
    def printTree(self, indent=0):
        print("  " * indent + "VECTOR")
        for row in self.matrix_rows:
            row.printTree(indent + 1)

    @addToClass(AST.MatrixRow)
    def printTree(self, indent=0):
        print("  " * indent + "VECTOR")
        for value in self.value:
            value.printTree(indent + 1)

    # IF - THEN - ELSE
    @addToClass(AST.IfExpr)
    def printTree(self, indent=0):
        print("  " * indent + "IF")
        self.condition.printTree(indent + 1)
        print("  " * indent + "THEN")
        self.block.printTree(indent + 1)
        if self.ifx:
            self.ifx.printTree(indent)


    @addToClass(AST.ElseExpr)
    def printTree(self, indent=0):
        print("  " * indent + "ELSE")
        self.block.printTree(indent + 1)

    # PĘTLE FOR I WHILE
    @addToClass(AST.ForLoopExpr)
    def printTree(self, indent=0):
        print("  " * indent + "FOR")
        self.loop_variable.printTree(indent + 1)
        self.range_expr.printTree(indent + 1)
        for b in self.body:
            b.printTree(indent + 1)

    @addToClass(AST.WhileLoopExpr)
    def printTree(self, indent=0):
        print("  " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        for b in self.body:
            b.printTree(indent + 1)

    # WYRAŻENIA BREAK, CONTINUE, RETURN
    @addToClass(AST.BreakExpr)
    def printTree(self, indent=0):
        print("  " * indent + "BREAK")

    @addToClass(AST.ContinueExpr)
    def printTree(self, indent=0):
        print("  " * indent + "CONTINUE")

    @addToClass(AST.ReturnExpr)
    def printTree(self, indent=0):
        print("  " * indent + "RETURN")
        self.val.printTree(indent + 1)

    # WYRAŻENIE PRINT
    @addToClass(AST.PrintExpr)
    def printTree(self, indent=0):
        print("  " * indent + "PRINT")
        for elem in self.val:
            elem.printTree(indent + 1)

    # RANGE
    @addToClass(AST.RangeExpr)
    def printTree(self, indent=0):
        print("  " * indent + "RANGE")
        self.startVal.printTree(indent + 1)
        self.endVal.printTree(indent + 1)

    @addToClass(AST.IndexRef)
    def printTree(self, indent=0):
        for num in self.value:
            num.printTree(indent)

    @addToClass(AST.MatrixIndexRef)
    def printTree(self, indent=0):
        print("  " * indent + 'REF')
        self.matrix.printTree(indent + 1)
        self.indices.printTree(indent + 1)

    # BŁĄD
    @addToClass(AST.Error)
    def printTree(self):
        print(self.message)
