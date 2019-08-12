class Queue:
    # Initialize an empty Queue
    def __init__(self):
        self.items = []

    # Insert an item to the queue so it is at the end of the stack
    def enqueue(self, item):
        self.items.append(item)

    # Take the first element from the beginning of the queue and return it
    def dequeue(self):
        return self.items.pop(0)

    # Returns true if empty, false if not empty
    def is_empty(self):
        return self.items == []

    def peek(self):
        if not self.is_empty():
            return self.items[0]

    # Return the iterable of the items in the queue, in order.
    def get_queue(self):
        return self.items
