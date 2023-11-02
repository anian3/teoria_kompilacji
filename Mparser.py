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
        p[0] = p[1] + p[3]
    elif p[2] == '.-':
        p[0] = p[1] - p[3]
    elif p[2] == '.*':
        p[0] = p[1] * p[3]
    elif p[2] == './':
        p[0] = p[1] / p[3]


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



parser = yacc.yacc()
