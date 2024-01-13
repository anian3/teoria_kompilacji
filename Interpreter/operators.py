import operator

import numpy as np

operators = {"+": operator.add,
             "-": operator.sub,
             "*": operator.mul,
             "/": lambda x, y: x / y,
             ".+": lambda x, y: x + y,
             ".-": lambda x, y: x - y,
             ".*": lambda x, y: x * y,
             "./": lambda x, y: x / y,
             ">": lambda x, y: x > y,
             "<": lambda x, y: x < y,
             ">=": lambda x, y: x >= y,
             "!=": lambda x, y: x != y,
             "<=": lambda x, y: x <= y,
             "==": lambda x, y: x == y,
             "eye": lambda x: np.eye(x),
             "zeros": lambda x: np.zeros(x),
             "ones": lambda x: np.ones(x),
             }
