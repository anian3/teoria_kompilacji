#!/usr/bin/python

import scanner
import ply.yacc as yacc
from AST import *

tokens = scanner.tokens

# Zasady parsingu
precedence = (
    ("nonassoc", 'IF'),
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
                  | printInstruction ';'
                  | assignmentInstruction ';'
                  | loop
                  | condition """
    if len(p) == 4 and p[1] == '{':
        p[0] = p[2]
    else:
        p[0] = p[1]


# 0.
def p_constant(p):
    """ expression : idConstant
                | intConstant
                | stringConstant
                | floatConstant """
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


# 1. Wyrażenia binarne (w tym macierzowe)
def p_expression_binop(p):
    """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression """
    p[0] = BinExpr(p[2], p[1], p[3])


def p_expression_binop_matrix(p):
    """ expression : expression DOTADD expression
                   | expression DOTSUB expression
                   | expression DOTMUL expression
                   | expression DOTDIV expression """
    p[0] = BinExpr(p[2], p[1], p[3])


# 2. Wyrażenia relacyjne
def p_expression_compare(p):
    """ expression : expression '>' expression
                    | expression '<' expression
                    | expression MOREEQ expression
                    | expression NOTEQ expression
                    | expression LESSEQ expression
                    | expression EQUAL expression """
    p[0] = CompExpression(p[2], p[1], p[3])


# 3. Negacja unarna
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = UMinExpression(p[1], p[2])


# 4. Transpozycja macierzy
def p_expression_transpose(p):
    """ expression : idConstant "'" """
    p[0] = TransposeExpression(p[2], p[1])


# 5. Inicjalizacja macierzy konkretnymi wartościami
def p_matrix_initialization(p):
    """ expression : '[' matrix_rows ']' """
    p[0] = MatrixInitWithValues(p[2])


def p_matrix_rows(p):
    """ matrix_rows :  matrix_row  """
    p[0] = [p[1]]


def p_matrix_rows_multiple(p):
    """ matrix_rows : matrix_rows ',' matrix_row """
    p[0] = p[1] + [p[3]]


def p_matrix_row(p):
    """ matrix_row : '['  matrix_row_values ']' """
    p[0] = MatrixRow(p[2])


def p_matrix_row_values(p):
    """  matrix_row_values : expression """
    p[0] = [p[1]]


def p_matrix_row_values_multiple(p):
    """ matrix_row_values : matrix_row_values ',' expression """
    p[0] = p[1] + [p[3]]


# 6. Macierzowe funkcje specjalne
def p_expression_matrix_special(p):
    """ expression : ZEROS '(' intConstant ')'
                    | EYE '(' intConstant ')'
                    | ONES '(' intConstant ')' """
    p[0] = MatrixInitFuncExpr(p[1], p[3])


# 7. Instrukcje przypisania
def p_expression_eq_assign(p):
    """ assignmentInstruction : idConstant '=' expression
                            | idConstant '=' matrix_row
                            | matrix_index_ref '=' expression """
    p[0] = AssignExpr(p[2], p[1], p[3])


def p_expression_assign(p):
    """ assignmentInstruction : expression ADDASSIGN expression
                   | expression SUBASSIGN expression
                   | expression MULASSIGN expression
                   | expression DIVASSIGN expression """
    p[0] = AssignExpr(p[2], p[1], p[3])


def p_index_expr(p):
    """ index_expr : intConstant
                    | intConstant ',' intConstant """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1], p[3]]


def p_matrix_index_ref(p):
    """ matrix_index_ref : idConstant '[' index_expr ']' """
    p[0] = MatrixIndexRef(p[1], IndexRef(p[3]))


# 8. Instrukcja warunkowa if-else
def p_expression_if(p):
    """ condition : IF expression statement ifx
                    | IF expression '{' statement '}' ifx"""
    if p[3] == '{':
        p[0] = IfExpr(p[2], p[4], p[6])
    else:
        p[0] = IfExpr(p[2], p[3], p[4])


def p_expression_ifx(p):
    """ ifx : ELSE statement
            | """
    if len(p) > 2:
        p[0] = ElseExpr(p[2])
    else:
        p[0] = None


# 9. Pętle while i for
# 10. Instrukcje break, continue, return
def p_expression_loop(p):
    """ loop : FOR idConstant '=' range statement
              | WHILE '(' expression ')' statement """
    if p[1] == 'for':
        p[0] = ForLoopExpr(p[2], p[4], p[5])
    elif p[1] == 'while':
        p[0] = WhileLoopExpr(p[3], p[5])


def p_inloop_extra(p):
    """ expression : BREAK
                    | CONTINUE """
    if p[1] == "break":
        p[0] = BreakExpr()
    else:
        p[0] = ContinueExpr()


def p_expression_return(p):
    """ expression : RETURN
                    | RETURN expression"""
    if len(p) == 3:
        p[0] = ReturnExpr(p[2])
    else:
        p[0] = ReturnExpr(None)


# 11. Instrukcja print
def p_expression_print(p):
    """ printInstruction : PRINT expression
                         | PRINT matrix_row_values """
    if type(p[2]) == list:
        p[0] = PrintExpr(p[2])
    else:
        p[0] = PrintExpr([p[2]])


# 12. Instrukcje złożone
def p_expression_group(p):
    """ expression : '(' expression ')' """
    p[0] = p[2]


# 13. Tablice oraz ich zakresy
def p_expression_range(p):
    """ range : expression ':' expression """
    p[0] = RangeExpr(p[1], p[3])


parser = yacc.yacc()
