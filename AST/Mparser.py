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
    if len(p) == 3 and p[1] == '{':
        p[0] = p[2]
    else:
        p[0] = p[1]


# 0.
def p_expression_id(p):
    """ expression : ID """
    p[0] = Variable(p[1])


def p_expression_string(p):
    """expression : STRING """
    p[0] = String(p[1])


def p_expression_int(p):
    """expression : INTNUM """
    p[0] = IntNum(p[1])


def p_expression_float(p):
    """expression : FLOATNUM"""
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
    p[0] = MatExpr(p[2], p[1], p[3])


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
    """ expression : ID "'" """
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
    """ expression : ZEROS '(' INTNUM ')'
                    | EYE '(' INTNUM ')'
                    | ONES '(' INTNUM ')' """
    p[0] = MatrixInitFuncExpr(p[1], p[3])


# def p_expression_matrix_set_values(p):
#     """ expression : matrix_value '=' expression """
#     if p[1] not in names:
#         raise SyntaxError("Unknown matrix")
#     p[0] = p[8]
#
#
# def p_expression_matrix_values(p):
#     """ matrix_value : ID '[' INTNUM ',' INTNUM ']' """
#     if p[1] not in names:
#         raise SyntaxError("Unknown matrix")
#     p[0] = names[p[1]][p[3]][p[5]]


# 7. Instrukcje przypisania
def p_expression_eq_assign(p):
    """ assignmentInstruction : expression '=' expression """
    p[0] = AssignExpr(p[2], p[1], p[3])


def p_expression_assign(p):
    """ assignmentInstruction : expression ADDASSIGN expression
                   | expression SUBASSIGN expression
                   | expression MULASSIGN expression
                   | expression DIVASSIGN expression """
    p[0] = AssignExpr(p[2], p[1], p[3])


# 8. Instrukcja warunkowa if-else
def p_expression_if(p):
    """ condition : IF expression statement ifx """
    if len(p) < 5:
        p[0] = IfExpr(p[1], p[2], p[3])
    else:
        p[0] = IfExpr(p[2], p[3], p[4])


def p_expression_ifx(p):
    """ ifx : ELSE condition
            | ELSE statement
            | """
    if type(p[2]) == IfExpr:
        p[0] = ElseIfExpr("ElSE IF", p[2])
    else:
        p[0] = ElseExpr("ELSE", p[2])


# 9. Pętle while i for
# 10. Instrukcje break, continue, return
def p_expression_loop(p):
    """ loop : FOR ID '=' range statement
              | WHILE '(' expression ')' statement """
    if p[1] == 'for':
        p[0] = ForLoopExpr(p[2], p[4], p[5])
    elif p[1] == 'while':
        p[0] = WhileLoopExpr(p[3], p[5])


def p_inloop_extra(p):
    """ expression : BREAK statement
                    | CONTINUE statement """
    if p[1] == "BREAK":
        p[0] = BreakExpr()
    else:
        p[0] = ContinueExpr()


def p_expression_extra(p):
    """ expression : RETURN
                    | RETURN expression"""
    if len(p) == 3:
        p[0] = ReturnExpr(p[2])
    else:
        p[0] = ReturnExpr(None)


# 11. Instrukcja print
def p_expression_print(p):
    """ printInstruction : PRINT expression """
    p[0] = PrintExpr(p[2])


# 12. Instrukcje złożone
def p_expression_group(p):
    """ expression : '(' expression ')' """
    p[0] = p[2]


# 13. Tablice oraz ich zakresy
def p_expression_range(p):
    """ range : expression ':' expression """
    p[0] = RangeExpr(p[1], p[3])


def p_index_expr(p):
    """ index_expr : INTNUM
                    | index_expr ',' INTNUM """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_matrix_index_ref(p):
    """ expression : ID '[' index_expr ']' """
    p[0] = MatrixIndexRef(p[1], IndexRef(p[3]))


def p_expression_list(p):
    """ expression : '[' list_values ']' """
    p[0] = ListInit(p[2])


def p_list_values_multiple(p):
    """ list_values : expression
                    | list_values ',' expression """
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


parser = yacc.yacc()
