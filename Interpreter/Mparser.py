#!/usr/bin/python

import scanner
import ply.yacc as yacc
from AST import *

tokens = scanner.tokens

# Zasady parsingu
precedence = (
    ("nonassoc", 'IFX'),
    ("nonassoc", 'ELSE'),
    ("nonassoc", '<', '>', 'LESSEQ', 'MOREEQ', 'NOTEQ', 'EQUAL'),
    ("left", '+', '-', 'DOTADD', 'DOTSUB'),
    ("left", 'DOTMUL', 'DOTDIV', '*', '/'),
    ("right", 'UMINUS', "'")
)

# Słownik nazw zmiennych
names = {}


# Błąd
def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


# Początek
def p_start(p):
    """ start : statements """
    p[0] = Program(p[1])


def p_statements(p):
    """ statements : statement
                   | statements statement """
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_statement(p):
    """ statement : expression ';'
                  | '{' statements '}'
                  | loop
                  | assignmentInstruction ';'
                  | returnExpression ';'
                  | printExpression ';'
                  | condition
                  """
    if len(p) == 4 and p[1] == '{':
        p[0] = p[2]
    else:
        p[0] = p[1]


# Zmienne
def p_constant(p):
    """ expression : idConstant
                | groupExpression
                | intConstant
                | stringConstant
                | floatConstant
                | vector """
    p[0] = p[1]


def p_expression_id(p):
    """ idConstant : ID """
    p[0] = Variable(p[1])


def p_expression_string(p):
    """ stringConstant : STRING """
    p[0] = String(p[1])


def p_expression_int(p):
    """ intConstant : INTNUM """
    p[0] = IntNum(p[1])


def p_expression_float(p):
    """ floatConstant : FLOATNUM"""
    p[0] = FloatNum(p[1])


# Wyrażenia binarne (w tym macierzowe)
def p_expression_binop(p):
    """ expression : expression '+' expression
                    | expression '-' expression
                    | expression '*' expression
                    | expression '/' expression
                    | expression DOTADD expression
                    | expression DOTSUB expression
                    | expression DOTMUL expression
                    | expression DOTDIV expression
                    """
    p[0] = BinExpr(p[2], p[1], p[3], p.lineno(2))


# Wyrażenia relacyjne
def p_expression_compare(p):
    """ expression : expression '>' expression
                    | expression '<' expression
                    | expression MOREEQ expression
                    | expression NOTEQ expression
                    | expression LESSEQ expression
                    | expression EQUAL expression """
    p[0] = CompExpression(p[2], p[1], p[3], p.lineno(2))


# Negacja unarna
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = UMinExpression(p[1], p[2], p.lineno(1))


# Transpozycja macierzy
def p_expression_transpose(p):
    """ expression : idConstant "'" """
    p[0] = TransposeExpression(p[2], p[1], p.lineno(1))


# Macierze
def p_expression_vector(p):
    """ vector : '['  vector_values ']' """
    p[0] = VectorInitWithValues(p[2], p.lineno(1))


def p_vector_values(p):
    """ vector_values : vector_values ',' expression
                        | expression
                        | vector_value
                        | """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_index_expr(p):
    """ index_expr : intConstant
                    | range
                    | intConstant ',' intConstant
                    | range ',' intConstant
                    | intConstant ',' range
                    | range ',' range """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1], p[3]]


def p_vector_value(p):
    """ vector_value : idConstant '[' index_expr ']'"""
    p[0] = MatrixIndexRef(p[1], IndexRef(p[3], p.lineno(3)), p.lineno(2))


def p_expression_matrix_special(p):
    """ expression : ZEROS '(' index_expr ')'
                    | EYE '(' index_expr ')'
                    | ONES '(' index_expr ')' """
    p[0] = MatrixInitFuncExpr(p[1], IndexRef(p[3], p.lineno(3)), p.lineno(1))


# Instrukcje przypisania
def p_expression_eq_assign(p):
    """ assignmentInstruction : idConstant '=' expression
                              | vector_value '=' expression
                              | vector_value '=' vector_value
                              | idConstant '=' vector_value
                              | expression ADDASSIGN expression
                              | expression SUBASSIGN expression
                              | expression MULASSIGN expression
                              | expression DIVASSIGN expression  """
    p[0] = AssignExpr(p[2], p[1], p[3], p.lineno(2))


# Instrukcje złożone
def p_expression_group(p):
    """ groupExpression : '(' expression ')' """
    p[0] = p[2]


# Zakres
def p_expression_range(p):
    """ range : intConstant ':' intConstant
                | idConstant ':' intConstant
                | idConstant ':' idConstant
                | intConstant ':' idConstant """
    p[0] = RangeExpr(p[1], p[3], p.lineno(2))


# Return / Print
def p_print(p):
    """ printExpression : PRINT vector_values """
    p[0] = PrintExpr(p[2], p.lineno(1))


def p_return(p):
    """ returnExpression : RETURN vector_values """
    if len(p) == 3:
        p[0] = ReturnExpr([p[2]], p.lineno(1))
    else:
        p[0] = ReturnExpr(None, p.lineno(1))


# If-else
def p_expression_if(p):
    """ condition : IF groupExpression statement  %prec IFX
                  | IF groupExpression statement ELSE statement """
    if len(p) == 4:
         p[0] = IfExpr(p[2], p[3], None, p.lineno(1))
    else:
         p[0] = IfExpr(p[2], p[3], ElseExpr(p[5], p.lineno(4)), p.lineno(1))


# Loops
def p_expression_loop(p):
    """ loop : FOR idConstant '=' range statement
              | WHILE groupExpression statement """
    if p[1] == 'for':
        p[0] = ForLoopExpr(p[2], p[4], p[5], p.lineno(1))
    elif p[1] == 'while':
        p[0] = WhileLoopExpr(p[2], p[3], p.lineno(1))


def p_inloop_extra(p):
    """ expression : BREAK
                    | CONTINUE """
    if p[1] == "break":
        p[0] = BreakExpr()
        p[0] = BreakExpr()
    else:
        p[0] = ContinueExpr()


# parser = yacc.yacc()