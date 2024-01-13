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
             "eye": lambda *args: np.eye(args[0] if len(args) == 1 else args),
             "zeros": lambda *args: np.zeros(args[0] if len(args) == 1 else args),
             "ones": lambda *args: np.ones(args[0] if len(args) == 1 else args),
             }
