from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

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
        print("  " * indent + str(self.value))

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
        self.value.printTree(indent + 1)

    @addToClass(AST.UMinExpression)
    def printTree(self, indent=0):
        print("  " * indent + "-")
        self.value.printTree(indent + 1)

    @addToClass(AST.AssignExpr)
    def printTree(self, indent=0):
        print("  " * indent + "-")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)
