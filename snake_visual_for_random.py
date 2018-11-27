from grid_for_ai import Grid
from queue import Queue
import user_input as ui
import turtle
import time
import random


class Gui():
    def __init__(self, grid_cols, grid_rows, grid):
        # Length and height (x,y) of the window. Each [row][col] in the grid is 20 pixels so we mult our grid sizes by 20
        self.length = grid_cols * 20
        self.height = grid_rows * 20
        self.grid_cols = grid_cols
        self.grid_rows = grid_rows
        self.frames = 10000
        self.got_food_score_change = -100
        self.died_score_change = 100000
        # Reference to the grid it came from
        self.grid = grid
        # Scores
        self.score = 0
        self.high_score = 0
        # Delay Timer so we don't go so fast!
        self.delay_start = 0.06
        # This is the seconds the game waits after death
        self.pause_delay = self.delay_start * 5
        self.delay = self.delay_start
        # The display window
        self.window = turtle.Screen()
        self.set_up_screen()
        # The snake head
        self.head = turtle.Turtle()
        self.set_snake_head()
        # The snake body (the tail)
        self.segments = []
        # The Food
        self.food = turtle.Turtle()
        self.set_food()
        # The score Baord (Drawn using a PEN)
        self.pen = turtle.Turtle()
        self.set_up_scoreboard()
        self.recursive_count = 0

    # Takes the indices of the 2d array and cover to coordinate points
    def convert_grid_to_coord(self, snake_node):
        x = (-(self.height/2)) + (snake_node.get_col() * 20)
        y = (self.length/2) + (-(snake_node.get_row()) * 20)
        return [x, y]

    # Update the score display
    def update_score_disp(self):
        self.pen.clear()
        self.pen.write("Score: {}  High Score: {}".format(self.score, self.high_score),
                       align="center", font=("Courier", 20, "normal"))

    # Hide and clear the tail so it isn't in the next round
    def hide_and_clear_segments(self):
        # Hide the segments
        for segment in self.segments:
            segment.goto(1000, 1000)
            segment.hideturtle()
        # Clear the segments list
        self.segments.clear()

    # Set Up the Screen
    def set_up_screen(self):
        self.window.title("Jack's Snake Game!")
        self.window.bgcolor("white")
        self.window.setup(width=self.length, height=self.height)
        self.window.tracer(0)  # Turns off screen updates

    # Sets up the Snake head. Places it in the center of the grid.
    def set_snake_head(self):
        self.head.speed(0)  # makes this as fast as possible
        self.head.shape("square")
        self.head.color("black")
        self.head.penup()
        x, y = self.convert_grid_to_coord(self.grid.head)
        self.head.goto(x, y)
        self.head.xdirection = 0
        self.head.ydirection = 0

    def add_segment(self):
        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("black")
        new_segment.penup()
        self.segments.append(new_segment)

    # Sets up the Snake Food
    def set_food(self):
        self.food.speed(0)
        self.food.shape("square")
        self.food.color("red")
        self.food.penup()
        x, y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)

    # Pen (for score board)
    def set_up_scoreboard(self):
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("black")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, (self.height / 2) - (self.height / 6))
        self.pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 20, "normal"))

    # Move the snake, and at any point if snake dead, break
    def move_snake(self):
        self.random_direction()
        self.recursive_count = 0
        row_move = self.head.xdirection
        col_move = self.head.ydirection
        self.grid.snake_move(row_move, col_move)
        # We did not die.
        if not self.grid.isdead:
            # We ate food, so food went to a new location, we grew, and moved
            if self.grid.grew:
                self.eat_and_grow()

            self.update_head_and_tail()
        # We did die. Reset the location of the snake head. restart.
        else:
            self.die()

    # This is what happens when we ate food! Yummy!
    def eat_and_grow(self):
        x, y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)
        self.add_segment()
        # Change the Score for getting an apple
        self.score += self.got_food_score_change
        self.update_score_disp()

    # This is what happens to move the snake around the board, head and body
    def update_head_and_tail(self):
        # New snake head location
        x, y = self.convert_grid_to_coord(self.grid.head)
        self.head.goto(x, y)
        # New tail locations
        i = 0
        for body_node in self.grid.tail.get_queue():
            x, y = self.convert_grid_to_coord(body_node)
            self.segments[i].goto(x, y)
            i += 1

    # This is what happens when a snake dies.
    def die(self):
        self.score += self.died_score_change
        self.recursive_count = 0
        self.grid.__init__(self.grid_rows, self.grid_cols)
        time.sleep(self.pause_delay)
        x, y = self.convert_grid_to_coord(self.grid.head)
        self.head.goto(x, y)
        x, y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)
        self.head.xdirection = 0
        self.head.ydirection = 1
        self.hide_and_clear_segments()
        # self.reset_score_and_delay()
        self.update_score_disp()

    # Change the direction of the snake to up
    def go_up(self):
        if self.recursive_count >= 30:
            self.die()
        elif self.head.xdirection == 1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction([False, True, True, True])
        else:
            self.head.xdirection = -1
            self.head.ydirection = 0

    # Change the direction of the snake to down
    def go_down(self):
        if self.recursive_count >= 30:
            self.die()
        elif self.head.xdirection == -1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction([True, False, True, True])
        else:
            self.head.xdirection = 1
            self.head.ydirection = 0

    # Change the direction of the snake to left
    def go_left(self):
        if self.recursive_count >= 30:
            self.die()
        elif self.head.ydirection == 1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction([True, True, False, True])
        else:
            self.head.xdirection = 0
            self.head.ydirection = -1

    # Change the direction of the snake to right
    def go_right(self):
        if self.recursive_count >= 30:
            self.die()
        elif self.head.ydirection == -1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction([True, True, True, False])
        else:
            self.head.xdirection = 0
            self.head.ydirection = 1

    def move_food_random(self):
        # Move the food to random spot
        self.grid.spawn_food()
        x, y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)

    # Bool Array Is for up, down, left, right, if this is a legal move!
    def choose_smart(self, worked):
        snake_x, snake_y = self.grid.head.get_node()
        food_x, food_y = self.grid.food_location.get_node()

        if snake_x < food_x and worked[0] and not self.put_in_box(1):
            self.go_down()
        elif snake_x > food_x and worked[1] and not self.put_in_box(0):
            self.go_up()
        else:
            if snake_y < food_y and worked[3] and not self.put_in_box(3):
                self.go_right()
            elif snake_y > food_y and worked[2] and not self.put_in_box(2):
                self.go_left()

    # Direction is up = 0, down = 1, left = 2, right = 3. We want to determine if that will put us in a box
    # Returns true if it will put in box and false if not in box
    def put_in_box(self, direction):
        snake_x, snake_y = self.grid.head.get_node()
        is_left = False
        is_right = False
        is_up = False
        is_down = False
        # Go Through all the tails and see if we will box ourself in with the border and our tail.
        for node in self.grid.tail.get_queue():
            node_x, node_y = node.get_node()
            # Tail is below the head and this is the first time that we learn this. Also we arn't at a border
            if not is_down and (snake_y == node_y and snake_x < node_x or snake_x == self.grid_rows - 1):
                is_down = True
            # Tail is above the head and this is the first time that we learn this. Also we arn't at a border
            if not is_up and (snake_y == node_y and snake_x > node_x or snake_x == 0):
                is_up = True
            # Tail is right of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_right and (snake_x == node_x and snake_y < node_y or snake_y == self.grid_cols - 1):
                is_right = True
            # Tail is left of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_left and (snake_x == node_x and snake_y > node_y or snake_y == 0):
                is_left = True
            # Return true if we are surrounded
            if is_up and is_down and is_left and is_right:
                return True
        # if we care about Up
        if direction == 0 and is_up and is_left and is_right:
            print("thinks it shouldn't go up")
            return True
        # if we care about Down
        elif direction == 1 and is_down and is_left and is_right:
            print("thinks it shouldn't go down")
            return True
        # if we care about Left
        elif direction == 2 and is_up and is_down and is_left:
            print("thinks it shouldn't go left")
            return True
        # if we care about Right
        elif direction == 3 and is_up and is_down and is_right:
            print("thinks it shouldn't go right")
            return True
        else:
            return False

    # Bool Array Is for down, up, right, left, if this is a legal move! (now y before x)
    def choose_smart_backward(self, worked):
        snake_x, snake_y = self.grid.head.get_node()
        food_x, food_y = self.grid.food_location.get_node()

        if snake_y < food_y and worked[2]:
            self.go_right()
        elif snake_y > food_y and worked[3]:
            self.go_left()
        else:
            if snake_x < food_x and worked[0]:
                self.go_down()
            elif snake_x > food_x and worked[1]:
                self.go_up()

    # Returns True if we are surrounded by the tail,
    # Retrns False if there is a way out.
    # When Returned with False, Then current x/y direction will be safe
    def surrounded(self):   # THIS PART IS BUGGY!
        snake_x, snake_y = self.grid.head.get_node()
        is_left = False
        is_right = False
        is_up = False
        is_down = False
        for node in self.grid.tail.get_queue():
            node_x, node_y = node.get_node()
            # Tail is below the head and this is the first time that we learn this. Also we arn't at a border
            if not is_down and (snake_y == node_y and snake_x < node_x or snake_x == self.grid_rows - 1):
                print('there is a tail down at {}'.format(node.get_node()))
                is_down = True
            # Tail is above the head and this is the first time that we learn this. Also we arn't at a border
            if not is_up and (snake_y == node_y and snake_x > node_x or snake_x == 0):
                print('there is a tail up at {}'.format(node.get_node()))
                is_up = True
            # Tail is right of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_right and (snake_x == node_x and snake_y < node_y or snake_y == self.grid_cols - 1):
                print('there is a tail right at {}'.format(node.get_node()))
                is_right = True
            # Tail is left of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_left and (snake_x == node_x and snake_y > node_y or snake_y == 0):
                print('there is a tail left at {}'.format(node.get_node()))
                is_left = True
            # Return true if we are surrounded
            if is_up and is_down and is_left and is_right:
                return True
        if not is_left:
            print('we chose left. {},{} as before move'.format(self.head.xdirection, self.head.ydirection))
            self.go_left()
        elif not is_up:
            print('we chose up. {},{} as before move'.format(self.head.xdirection, self.head.ydirection))
            self.go_up()
        elif not is_right:
            print('we chose right. {},{} as before move'.format(self.head.xdirection, self.head.ydirection))
            self.go_right()
        elif not is_down:
            print('we chose down. {},{} as before move'.format(self.head.xdirection, self.head.ydirection))
            self.go_down()
        # Return false if we are not surrounded
        return False

    def smart_direction(self, worked=[True, True, True, True]):
        print('increasing recursive count to {}'.format(self.recursive_count))
        self.recursive_count += 1
        if self.recursive_count <= 10:
            self.choose_smart(worked)
        row_move = self.head.xdirection
        col_move = self.head.ydirection
        while not self.grid.snake_check_move(row_move, col_move):
            print('stuck here with {},{}'.format(self.head.xdirection, self.head.ydirection))
            if row_move == col_move and self.recursive_count >= 30:
                self.die()
            if self.surrounded():
                print('increasing recursive count to {}'.format(self.recursive_count))
                self.recursive_count += 1
                print('is surrounded')
                rand_direction = random.randint(0, 3)   # THIS IS THE LAST THING I NEED TO DO
                # CHANGE HOW RANDOM DISISIONS ARE DONE WHEN NOTHING LOOKS LIKE A GOOD MOVE
                # HINT: PROBABLY NEEDS TO GO TO THE SIDE WITH THE FURTHEST TAIL DISTANCE
                # AKA DONT MOVE TO THE SIDE WITH THE TAIL THAT IS ONE BLOCK AWAY BUT THE ONE
                # THAT IS A COUPLE SPACES AWAY. GIVES MORE BREATHEING ROOM
                print(rand_direction)
                if rand_direction == 0:
                    self.go_up()
                elif rand_direction == 1:
                    self.go_down()
                elif rand_direction == 2:
                    self.go_left()
                elif rand_direction == 3:
                    self.go_right()
            row_move = self.head.xdirection
            col_move = self.head.ydirection
            print('try {},{}'.format(self.head.xdirection, self.head.ydirection))
            # For redundancy purposes
            row_move = self.head.xdirection
            col_move = self.head.ydirection

    def random_direction(self):
        rand_direction = random.randint(0, 3)
        self.recursive_count += 1
        if rand_direction == 0:
            self.go_up()
        elif rand_direction == 1:
            self.go_down()
        elif rand_direction == 2:
            self.go_left()
        elif rand_direction == 3:
            self.go_right()
        row_move = self.head.xdirection
        col_move = self.head.ydirection

        while not self.grid.snake_check_move(row_move, col_move):
            rand_direction = random.randint(0, 3)
            if rand_direction == 0:
                self.go_up()
            elif rand_direction == 1:
                self.go_down()
            elif rand_direction == 2:
                self.go_left()
            elif rand_direction == 3:
                self.go_right()
            row_move = self.head.xdirection
            col_move = self.head.ydirection

    def print_grid(self):
        index = 0
        for element in self.grid.grid:
            print(element, end=' ')
            print(index)
            index += 1
        print()


grid_rows = 30
grid_cols = 30

# Create Grid, Initialize Snake head, Spawn Food
g = Grid(grid_rows, grid_cols)

gui = Gui(grid_cols, grid_rows, g)

# Main Game Loop. Runs for a total number of frames
for _ in range(gui.frames):
    gui.score += 1
    gui.update_score_disp()
    gui.window.update()
    gui.print_grid()
    # move the snake through the grid.
    gui.move_snake()

    # Pause the execution of the program so it doesn't go lightning fast
    # time.sleep(gui.delay)

gui.window.mainloop()
