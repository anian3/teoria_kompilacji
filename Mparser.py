#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    ("nonassoc", '=', '+=', '-=', '*=', '/=', '<', '>', '<=', '>=', '!=', '=='),
    ("nonassoc", ':'),
    ("left", '+', '-', '.+', '.-'),
    ("left", '.*', './', '*', '/'),
    ("right", '-'),
    ("left", '(', ')', '[', ']', '{', '}')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_expression_binop(p):
    """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression"""
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_binop_matrix(p):
    if p[2] == '.+':
        p[0] = p[1] + p[3]
    elif p[2] == '.-':
        p[0] = p[1] - p[3]
    elif p[2] == '.*':
        p[0] = p[1] * p[3]
    elif p[2] == './':
        p[0] = p[1] / p[3]


def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


# to finish the grammar
# ....


parser = yacc.yacc()
