#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

# Parsing rules
precedence = (
    ("nonassoc", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', '<', '>', 'LESSEQ', 'MOREEQ', 'NOTEQ',
     'EQUAL'),
    ("nonassoc", ':'),
    ("left", '+', '-', 'DOTADD', 'DOTSUB'),
    ("left", 'DOTADD', 'DOTDIV', '*', '/'),
    ("right", 'UMINUS'),
    ("left", '(', ')', '[', ']', '{', '}')
)

# dictionary of names
names = {}


def p_statement_assign(t):
    """statement : ID '=' expression"""
    names[t[1]] = t[3]


def p_statement_expr(t):
    """ statement : expression """
    print(t[1])


def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = -p[2]


def p_expression_binop(p):
    """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression """
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[1] == '-':
        p[0] = - p[2]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_binop_matrix(p):
    """ expression : expression DOTADD expression
                   | expression DOTSUB expression
                   | expression DOTMUL expression
                   | expression DOTDIV expression """
    if p[2] == '.+':
        p[0] = matrix_addition(p[1], p[3])
    elif p[2] == '.-':
        p[0] = matrix_substraction(p[1], p[3])
    elif p[2] == '.*':
        p[0] = matrix_multiplication(p[1], p[3])
    elif p[2] == './':
        p[0] = matrix_division(p[1], p[3])


def p_expression_assign(p):
    """ expression : expression ADDASSIGN expression
                   | expression SUBASSIGN expression
                   | expression MULASSIGN expression
                   | expression DIVASSIGN expression """
    if p[2] == '+=':
        p[1] += p[3]
    elif p[2] == '-=':
        p[1] -= p[3]
    elif p[2] == '*=':
        p[1] *= p[3]
    elif p[2] == '/=':
        p[1] /= p[3]


def p_expression_transpose(p):
    """ expression: "'" expression """
    p[0] = matrix_transpose(p[1])


def p_matrix_initialization(p):
    """ expression : '[' matrix_rows ']' """
    p[0] = p[2]


def p_matrix_rows(p):
    """matrix_rows :  matrix_row_values  """
    p[0] = [p[1]]


def p_matrix_rows_multiple(p):
    """matrix_rows : matrix_rows ',' matrix_row_values """
    p[0] = p[1] + [p[3]]


def p_matrix_row_values(p):
    """matrix_row_values : matrix_row_values ',' expression
                            | matrix_row_values """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_expression_group(t):
    """ expression : '(' expression ')'
                   | '[' expression ']'
                   | '{' expression '}'
                    """
    t[0] = t[2]


def p_expression_id(t):
    'expression : ID'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


def p_expression_float(t):
    'expression : FLOATNUM'
    t[0] = t[1]


def p_expression_int(t):
    'expression : INTNUM'
    t[0] = t[1]


def p_expression_string(t):
    'expression : STRING'
    t[0] = t[1]


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


# def p_program(p):
#     """program : instructions_opt"""

# funkcje pomocnicze

def matrix_addition(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Dodawanie element po elemencie na różnych rozmiarach macierzy.")
        return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Dodawanie macierzowe wykonywane nie na macierzach.")


def matrix_substraction(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Odejmowanie element po elemencie na różnych rozmiarach macierzy.")
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Odejmowanie macierzowe wykonywane nie na macierzach.")


def matrix_multiplication(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Mnożenie element po elemencie na różnych rozmiarach macierzy.")
        return [[A[i][j] * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Mnożenie macierzowe wykonywane nie na macierzach.")


def matrix_division(A, B):
    if isinstance(A, list) and isinstance(B, list):
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Dzielenie element po elemencie na różnych rozmiarach macierzy.")
        for i in range(len(B)):
            for j in range(len(B[0])):
                if B[i][j] == 0:
                    raise ValueError("Dzielenie przez zero.")
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    else:
        raise ValueError("Odejmowanie macierzowe wykonywane nie na macierzach.")


def matrix_transpose(A):
    if isinstance(A, list):
        return [[row[i] for row in A] for i in range(len(A[0]))]
    else:
        raise ValueError("Transpozycja wykonywana nie dla macierzy.")


parser = yacc.yacc()
