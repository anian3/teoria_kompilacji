class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.symbols = {}

    def has_key(self, name):  # variable name
        return name in self.symbols

    def get(self, name):  # gets from memory current value of variable <name>
        return self.symbols.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.symbols[name] = value


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.memory_stack = [Memory('global') if memory is None else memory]

    def get(self, name):  # gets from memory stack current value of variable <name>
        for memory in reversed(self.memory_stack):
            val = memory.get(name)
            if val is not None:
                return val
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        for stack in self.memory_stack:
            if stack.has_key(name):
                stack.put(name, value)
                return
        self.memory_stack[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        for memory in reversed(self.memory_stack):
            if memory.has_key(name):
                memory.put(name, value)
                break
        return None

    def push(self, memory):  # pushes memory <memory> onto the stack
        self.memory_stack.append(memory)

    def pop(self):  # pops the top memory from the stack
        self.memory_stack.pop()
