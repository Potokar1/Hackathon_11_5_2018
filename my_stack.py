# Modifies a python List
class Stack:
    # Initialization of an empty Stack
    def __init__(self):
        self.items = []

    # insert an item to the stack so it is on the top of the stack
    def push(self, item):
        self.items.append(item)

    # Take the top item off the stack and return it.
    def pop(self):
        return self.items.pop()

    # Check to see if the stack is empty.
    def is_empty(self):
        return self.items == []

    # take a look at the top of the stack without removing.
    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    # Returns all of the items in the stack.
    def get_stack(self):
        return self.items