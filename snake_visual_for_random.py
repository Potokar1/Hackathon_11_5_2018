from grid_for_ai import Grid
from queue import Queue
import user_input as ui
import turtle
import time
import random

grid_rows = 10
grid_cols = 10

# Create Grid, Initialize Snake head, Spawn Food
g = Grid(grid_rows, grid_cols)


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
        self.delay_start = 0.5
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
        self.smart_direction()
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
        self.head.ydirection = 0
        self.hide_and_clear_segments()
        # self.reset_score_and_delay()
        self.update_score_disp()

    # Change the direction of the snake to up
    def go_up(self):
        if self.recursive_count > 50:
            self.die()
        elif self.head.xdirection == 1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction()
        else:
            self.head.xdirection = -1
            self.head.ydirection = 0

    # Change the direction of the snake to down
    def go_down(self):
        if self.recursive_count > 50:
            self.die()
        elif self.head.xdirection == -1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction()
        else:
            self.head.xdirection = 1
            self.head.ydirection = 0

    # Change the direction of the snake to left
    def go_left(self):
        if self.recursive_count > 50:
            self.die()
        elif self.head.ydirection == 1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction()
        else:
            self.head.xdirection = 0
            self.head.ydirection = -1

    # Change the direction of the snake to right
    def go_right(self):
        if self.recursive_count > 50:
            self.die()
        elif self.head.ydirection == -1:
            # Try Again
            self.head.xdirection = 0
            self.head.ydirection = 0
            self.smart_direction()
        else:
            self.head.xdirection = 0
            self.head.ydirection = 1

    def move_food_random(self):
        # Move the food to random spot
        self.grid.spawn_food()
        x, y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)

    def choose_smart(self):
        snake_x, snake_y = self.grid.head.get_node()
        food_x, food_y = self.grid.food_location.get_node()
        if snake_x < food_x:
            self.go_down()
        elif snake_x > food_x:
            self.go_up()
        else:
            if snake_y < food_y:
                self.go_right()
            elif snake_y > food_y:
                self.go_left()


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
            # Tail is below of head
            if snake_y == node_y and snake_x < node_x or snake_x == self.grid_rows - 1:
                print('there is a tail down at {}'.format(node.get_node()))
                is_down = True
            if snake_y == node_y and snake_x > node_x or snake_x == 0:
                print('there is a tail up at {}'.format(node.get_node()))
                is_up = True
            if snake_x == node_x and snake_y < node_y or snake_y == self.grid_cols - 1:
                print('there is a tail right at {}'.format(node.get_node()))
                is_right = True
            if snake_x == node_x and snake_y > node_y or snake_y == 0:
                print('there is a tail left at {}'.format(node.get_node()))
                is_left = True
            # Return true if we are surrounded
            if is_up and is_down and is_left and is_right:
                return True
        if not is_left:
            print('we chose left')
            self.go_left()
        elif not is_up:
            print('we chose up')
            self.go_up()
        elif not is_right:
            print('we chose right')
            self.go_right()
        elif not is_down:
            print('we chose down')
            self.go_down()
        # Return false if we are not surrounded
        return False

    def smart_direction(self):
        self.recursive_count += 1
        self.choose_smart()
        row_move = self.head.xdirection
        col_move = self.head.ydirection
        while not self.grid.snake_check_move(row_move, col_move):
            print('stuck here')
            if self.surrounded():
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
            print('try {},{}'.format(self.head.xdirection,self.head.ydirection))

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
    time.sleep(gui.delay)

gui.window.mainloop()
