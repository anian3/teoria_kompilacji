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

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.op))
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.op))
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.CompExpression)
    def printTree(self, indent=0):
        print("  " * indent + str(self.op))
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.TransposeExpression)
    def printTree(self, indent=0):
        print("  " * indent + "TRANSPOSE")
        print("  " * (indent + 1) + str(self.value))

    @addToClass(AST.UMinExpression)
    def printTree(self, indent=0):
        print("  " * indent + "-")
        self.value.printTree(indent + 1)

    @addToClass(AST.AssignExpr)
    def printTree(self, indent=0):
        print("  " * indent + self.op)
        if isinstance(self.left, str):
            print("  " * indent + self.left)
        else:
            self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.MatrixInitFuncExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.func))
        print("  " * (indent + 1) + str(self.size))

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

    @addToClass(AST.ListInit)
    def printTree(self, indent=0):
        print("  " * indent + "LIST")
        for value in self.value:
            value.printTree(indent + 1)

    @addToClass(AST.IfExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.func))
        self.condition.printTree(indent + 1)
        self.block.printTree(indent + 1)
        self.ifx.printTree(indent)

    @addToClass(AST.ElseIfExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.func))
        self.block.condition.printTree(indent + 1)
        self.block.block.printTree(indent + 2)
        self.block.ifx.printTree(indent)

    @addToClass(AST.ElseExpr)
    def printTree(self, indent=0):
        print("  " * indent + str(self.func))
        self.block.printTree(indent + 1)

    @addToClass(AST.ForLoopExpr)
    def printTree(self, indent=0):
        print("  " * indent + "FOR")
        print("  " * (indent + 1) + f"{self.loop_variable}")
        self.range_expr.printTree(indent + 2)
        self.body.printTree(indent + 2)

    @addToClass(AST.WhileLoopExpr)
    def printTree(self, indent=0):
        print("  " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.body.printTree(indent + 2)

    @addToClass(AST.BreakExpr)
    def printTree(self, indent=0):
        print("  " * indent + self.func)

    @addToClass(AST.ContinueExpr)
    def printTree(self, indent=0):
        print("  " * indent + self.func)

    @addToClass(AST.ReturnExpr)
    def printTree(self, indent=0):
        print("  " * indent + self.func)
        self.val.printTree(indent + 1)

    @addToClass(AST.PrintExpr)
    def printTree(self, indent=0):
        print("  " * indent + self.func)
        if isinstance(self.val, str):
            print("  " * (indent + 1) + f'"{self.val}"')
        else:
            self.val.printTree(indent + 1)

    @addToClass(AST.RangeExpr)
    def printTree(self, indent=0):
        print("  " * indent + self.func)
        self.startVal.printTree(indent + 1)
        self.endVal.printTree(indent + 1)

    @addToClass(AST.IndexRef)
    def printTree(self, indent=0):
        for num in self.value:
            print("  " * indent + str(num))

    @addToClass(AST.MatrixIndexRef)
    def printTree(self, indent=0):
        print("  " * indent + 'REF')
        print("  " * (indent + 1) + str(self.matrix))
        self.indices.printTree(indent + 1)

    # @addToClass(AST.ListIndex)
    # def printTree(self, indent=0):
    #     print("  " * indent + 'REF')
    #     self.list.printTree(indent + 1)
    #     print("  " * (indent + 1) + str(self.index))
    #
    # @addToClass(AST.MatrixIndex)
    # def printTree(self, indent=0):
    #     print("  " * indent + 'REF')
    #     self.matrix.printTree(indent + 1)
    #     print("  " * (indent + 1) + str(self.row_index))
    #     print("  " * (indent + 1) + str(self.column_index))

    @addToClass(AST.Error)
    def printTree(self):
        print(self.message)
