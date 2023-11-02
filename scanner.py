import ply.lex as lex

literals = "+-*/()=<>[]{}':,;"

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT'
}

tokens = ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', 'FLOATNUM', 'INTNUM', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN',
             'DIVASSIGN', 'LESSEQ', 'MOREEQ', 'NOTEQ', 'EQUAL', 'STRING', 'ID'] + list(reserved.values())

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='
t_LESSEQ = r'<='
t_MOREEQ = r'>='
t_NOTEQ = r'!='
t_EQUAL = r'=='


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOATNUM(t):
    r'(\d*[.]\d+|\d+[.]\d*)([Ee][+-]?\d+)?'
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = str(t.value)[1:-1]
    return t


def t_COMMENT(t):
    r'\#.*'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
