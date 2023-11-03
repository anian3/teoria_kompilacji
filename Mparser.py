#!/usr/bin/python

import scanner
import ply.yacc as yacc

tokens = scanner.tokens


# Zasady parsingu
precedence = (
    ("nonassoc", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN', '<', '>', 'LESSEQ', 'MOREEQ', 'NOTEQ',
     'EQUAL'),
    ("nonassoc", ':'),
    ("left", '+', '-', 'DOTADD', 'DOTSUB'),
    ("left", 'DOTADD', 'DOTDIV', '*', '/'),
    ("right", 'UMINUS'),
    ("left", '(', ')', '[', ']', '{', '}')
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
    """ statement : expression ';' statement
                    | """
    pass


# 0.
def p_expression_id(p):
    """ expression : ID """
    print('Calling id: ' + p[1])
    if p[1] in names:
        p[0] = names[p[1]]
    else:
        raise SyntaxError("Unknown id")


def p_expression_value(p):
    """expression : STRING
                    | INTNUM
                    | FLOATNUM"""
    p[0] = p[1]


# 1. Wyrażenia binarne (w tym macierzowe)
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


# 2. Wyrażenia relacyjne
def p_expression_compare(p):
    """ expression : expression '>' expression
                    | expression '<' expression
                    | expression MOREEQ expression
                    | expression NOTEQ expression
                    | expression LESSEQ expression
                    | expression EQUAL expression """

    if p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    else:
        p[0] = p[1] <= p[3]


# 3. Negacja unarna
def p_expression_uminus(p):
    """expression : '-' expression %prec UMINUS"""
    p[0] = -p[2]


# 4. Transpozycja macierzy
def p_expression_transpose(p):
    """ expression : "'" expression """
    p[0] = matrix_transpose(p[1])



# 5. Inicjalizacja macierzy konkretnymi wartościami
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
                            | matrix_row_values
                             | expression """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# 6. Macierzowe funkcje specjalne
def p_expression_matrix_special(p):
    """ expression : ZEROS '(' INTNUM ')'
                    | EYE '(' INTNUM ')'
                    | ONES '(' INTNUM ')' """
    if p[0] == 'ZEROS':
        p[0] = [[0 for _ in range(p[3])] for _ in range(p[3])]
    elif p[0] == 'EYE':
        p[0] = [[0 if i != j else 1 for i in range(p[3])] for j in range(p[3])]
    elif p[0] == 'ONES':
        p[0] = [[1 for _ in range(p[3])] for _ in range(p[3])]


def p_expression_matrix_set_values(p):
    """ expression : ID '[' INTNUM ',' INTNUM ']' '=' expression """
    if p[1] not in names:
        raise SyntaxError("Unknown matrix")
    # names[p[1]][p[3]][p[5]] = p[8]
    p[0] = p[8]


def p_expression_matrix_values(p):
    """ expression : ID '[' INTNUM ',' INTNUM ']' """
    if p[1] not in names:
        raise SyntaxError("Unknown matrix")
    p[0] = names[p[1]][p[3]][p[5]]


# 7. Instrukcje przypisania
def p_expression_eq_assign(p):
    """ expression : ID '=' expression """
    print('New id: ' + p[1])
    names[p[1]] = p[3]


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


# 8. Instrukcja warunkowa if-else
def p_expression_if(p):
    """ expression : IF '(' expression ')' '{' statement '}' ELSE '{' expression '}' """
    if p[2]:
        p[0] = p[3]
    else:
        p[0] = p[5]


# 9. Pętle while i for
# 10. Instrukcje break, continue, return
def p_expression_loop(p):
    """ expression : FOR ID '=' INTNUM ':' INTNUM statement
                    | WHILE '(' expression ')' statement
                     | '{' statement '}'"""
    p[0] = p[3]


def p_expression_extra(p):
    """ expression : BREAK
                    | CONTINUE
                    | RETURN
                    | RETURN expression"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        pass


# 11. Instrukcja print
def p_expression_print(p):
    """ expression : PRINT STRING """
    p[0] = p[2]
    print(p[2])


# 12. Instrukcje złożone
def p_expression_group(p):
    """ expression : '(' expression ')'
                   | '[' expression ']'
                   | '{' expression '}' """
    p[0] = p[2]


# 13. Tablice oraz ich zakresy
def p_expression_range(p):
    """ expression : INTNUM ':' INTNUM """
    p[0] = [i for i in range(p[1], p[3]+1)]


# 14. Pozostałe

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
