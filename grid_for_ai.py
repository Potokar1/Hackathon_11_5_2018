# Used to get a random position for the apple and the snake head start.
import random
# random.seed(100)
from my_queue import Queue
from snake_node import Snake_Node

# The Grid object to create and manipulate the grid being played on.


class Grid():
    # initialize the Grid, Default height and length 20x20
    def __init__(self, height=20, length=20):
        self.height = height
        self.length = length
        self.grid = []
        self.grew = False
        self.head = Snake_Node(0, 0)
        self.temp_head = Snake_Node(0, 0)
        # Re-used snake node to keep location of food on grid
        self.food_location = Snake_Node(0, 0)
        # The tail is a queue of snake nodes
        self.tail = Queue()
        self.isdead = False
        self.create_grid()
        self.snake_head_start_location()
        self.spawn_food()

    # Set every node in the grid to zero
    def reset_grid(self):
        for row in range(self.height):
            for col in range(self.length):
                self.grid[row][col] = 0

    # Create a grid that is initialized to zero
    def create_grid(self):
        for row in range(self.height):
            self.grid.append([])
            for col in range(self.length):
                self.grid[row].append(0)

    # This is to update any given value on the grid.
    # 0 for empty
    # 1 for snake head
    # 2 for snake body
    # 3 for food
    def update_grid(self, row, col, value):
        self.grid[row][col] = value

    # This spawns food at a random location on the map not occupeied by other things
    def spawn_food(self):
        row = random.randint(0, self.height-1)
        col = random.randint(0, self.length-1)
        while self.grid[row][col] != 0:
            row = random.randint(0, self.height-1)
            col = random.randint(0, self.length-1)
        self.food_location = Snake_Node(row, col)
        self.update_grid(row, col, 3)

    # This spawns the snake head in the center of the grid
    def snake_head_start_location(self):
        start_row = random.randint(0, self.height-1)
        start_col = random.randint(0, self.length-1)
        self.head = Snake_Node(start_row, start_col)
        self.update_grid(start_row, start_col, 1)

    # The tail moves, It sheds its old tail end and has a new tail start
    def update_tail(self, head):
        self.tail.enqueue(head)
        self.update_grid(head.row, head.col, 2)
        # Snakes shed skin so this is the tail that it 'shed' as it moved
        shed = self.tail.dequeue()
        self.update_grid(shed.row, shed.col, 0)

    # The tail grows, It doesnt shed its old tail end and has a new tail start
    def grow(self, head):
        self.tail.enqueue(head)
        self.update_grid(head.row, head.col, 2)

    # The action of eating food makes the snake grow in size by one.
    def eat_food(self):
        self.grow(self.temp_head)

    # The action of slithering down the grid, not losing / gaining any length
    def move_tail(self):
        self.update_tail(self.temp_head)

    # Move the head to a new position (the rest of the snake will follow)
    def move_head(self, row_move, col_move):
        new_node = Snake_Node(self.head.row + row_move, self.head.col + col_move)
        self.head = new_node
        self.update_grid(new_node.row, new_node.col, 1)

    # This will move the snake. Only one move per 'turn', either row or col move, not both.
    def snake_move(self, row_move, col_move):
        # Checks to see if a move is legal, An illegal move does result in death!
        if self.snake_check_move(row_move, col_move):
            # Move is good, just moving through the grid
            if self.grid[self.head.row + row_move][self.head.col + col_move] == 0:
                self.grew = False
                self.temp_head = self.head
                self.move_head(row_move, col_move)
                self.move_tail()

            # Move is impossible, There is an error
            elif self.grid[self.head.row + row_move][self.head.col + col_move] == 1:
                self.grew = False

            # Move ends in death, Head hit the body
            elif self.grid[self.head.row + row_move][self.head.col + col_move] == 2:
                self.grew = False
                if self.grid[self.head.row + row_move][self.head.col + col_move] == 2:
                    self.dead()

            # Move makes the snake grow. We just ate food!!
            elif self.grid[self.head.row + row_move][self.head.col + col_move] == 3:
                self.grew = True
                self.temp_head = self.head
                self.move_head(row_move, col_move)
                self.eat_food()
                self.spawn_food()
        # The snake hit a wall
        else:
            self.grew = False
            self.dead()

    # Check to see if a move with cross the boundry. If bad move then DEAD
    # Returns true if legal move, Returns false if illegal move
    def snake_check_move(self, row_move, col_move):
        legal = True
        if row_move == 0 and col_move == 0:
            legal = False
            #print("From Grid: don't stay still")
            return legal
        # Top Row
        if self.head.row == 0:

            # Top Left Corner (No Moving left or up)
            if self.head.col == 0:
                if row_move == -1 or col_move == -1:
                    #print("From Grid: don't cross top left")
                    legal = False

            # Top Right Corner (No Moving Right or Up)
            elif self.head.col == self.length - 1:
                if row_move == -1 or col_move == 1:
                    #print("From Grid: don't cross top right")
                    legal = False

            # Top Row - no Corners (No Moving Up)
            else:
                if row_move == -1:
                    #print("From Grid: don't cross top")
                    legal = False

        # Bottom Row
        elif self.head.row == self.height - 1:

            # Bottom left corner (No moving down or left)
            if self.head.col == 0:
                if row_move == 1 or col_move == -1:
                    #print("From Grid: don't cross bottom left")
                    legal = False
            # Bottom Right Corner (No movin Down or Right)
            elif self.head.col == self.length - 1:
                if row_move == 1 or col_move == 1:
                    #print("From Grid: don't cross bottom right")
                    legal = False

            # Bottom Row - No Corners (No moving down)
            else:
                if row_move == 1:
                    #print("From Grid: don't cross bottom")
                    legal = False

        # Very Left - No corners (No moving left)
        elif self.head.col == 0:
            if col_move == -1:
                #print("From Grid: don't cross left")
                legal = False

        # Very Right - No Corners (No moving Right)
        elif self.head.col == self.length - 1:
            if col_move == 1:
                #print("From Grid: don't cross right")
                legal = False

        # If not_if_hitting_body returns false, then the snake WILL die , so it is not a legal move.
        if legal and not self.not_if_hitting_body(row_move, col_move):
            #print("From Grid: don't hit body")
            legal = False

        return legal

    # This will return TRUE if the snake hits a wall or itself. DEAD BOI
    def dead(self):
        self.isdead = True

    # This will return False if next move WILL hit self, and True if it WILL NOT
    def not_if_hitting_body(self, row_move, col_move):
        head_x, head_y = self.head.get_node()
        if self.grid[head_x + row_move][head_y + col_move] == 2:
            return False
        else:
            return True
