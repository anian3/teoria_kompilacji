import operator

import numpy as np

operators = {"+": operator.add,
             "-": operator.sub,
             "*": operator.mul,
             "/": lambda x, y: x / y,
             "DOTADD": lambda x, y: x + y,
             "DOTSUB": lambda x, y: x - y,
             "DOTMUL": lambda x, y: x * y,
             "DOTDIV": lambda x, y: x / y,
             ">": lambda x, y: x > y,
             "<": lambda x, y: x < y,
             "MOREEQ": lambda x, y: x >= y,
             "NOTEQ": lambda x, y: x != y,
             "LESSEQ": lambda x, y: x <= y,
             "EQUAL": lambda x, y: x == y,
             "EYE": lambda x: np.eye(x),
             "ZEROS": lambda x: np.zeros(x),
             "ONES": lambda x: np.ones(x),
             }
