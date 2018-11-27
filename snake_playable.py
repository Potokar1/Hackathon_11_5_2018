from old_grid import Grid
from queue import Queue
import user_input as ui
import turtle
import time
import random

grid_length = 30
grid_height = 30

# Create Grid, Initialize Snake head, Spawn Food
g = Grid(grid_length,grid_height)


class Gui():
    def __init__(self,grid_length,grid_height,grid):
        # Length and height (x,y) of the window. Each [row][col] in the grid is 20 pixels so we mult our grid sizes by 20
        self.length = grid_length * 20
        self.height = grid_height * 20
        self.grid_length = grid_length
        self.grid_height = grid_height
        # Reference to the grid it came from
        self.grid = grid
        # Scores
        self.score = 0
        self.high_score = 0
        # Delay Timer so we don't go so fast!
        self.delay_start = 0.05
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

    # Takes the indices of the 2d array and cover to coordinate points
    def convert_grid_to_coord(self,snake_node):
        x = (-300) + ( snake_node.get_col() * 20 )
        y = (300) + ( -(snake_node.get_row()) * 20 )
        return [x,y]

    # Update the score display
    def update_score_disp(self):
        self.pen.clear()
        self.pen.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center", font=("Courier", 20, "normal"))

    # Hide and clear the tail so it isn't in the next round
    def hide_and_clear_segments(self):
        # Hide the segments
        for segment in self.segments:
            segment.goto(1000,1000)
            segment.hideturtle()
        # Clear the segments list
        self.segments.clear()

    def reset_score_and_delay(self):
        # Reset the score
        self.score = 0
        # Reset the delay
        self.delay = self.delay_start

    # Set Up the Screen
    def set_up_screen(self):
        self.window.title("Jack's Snake Game!")
        self.window.bgcolor("white")
        self.window.setup(width=self.length, height=self.height)
        self.window.tracer(0) # Turns off screen updates
        # Keyboard Bindings
        self.window.listen()
        self.window.onkeypress(self.go_up, "w")
        self.window.onkeypress(self.go_down, "s")
        self.window.onkeypress(self.go_left, "a")
        self.window.onkeypress(self.go_right, "d")


    # Sets up the Snake head. Places it in the center of the grid.
    def set_snake_head(self):
        self.head.speed(0)
        self.head.shape("square")
        self.head.color("black")
        self.head.penup()
        x,y = self.convert_grid_to_coord(self.grid.head)
        self.head.goto(x,y)
        self.head.direction = "stop"

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
        x,y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)

    # Pen (for score board)
    def set_up_scoreboard(self):
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("black")
        self.pen.penup()
        self.pen.hideturtle()
        self.pen.goto(0, (self.height / 2 ) - 30 )
        self.pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 20, "normal"))

    """
        # Move the snake in a direction one unit
        def move(self):
            if self.head.direction == "up":
                y = self.head.ycor()
                self.head.sety(y + 20)
            if self.head.direction == "down":
                y = self.head.ycor()
                self.head.sety(y - 20)
            if self.head.direction == "left":
                x = self.head.xcor()
                self.head.setx(x - 20)
            if self.head.direction == "right":
                x = self.head.xcor()
                self.head.setx(x + 20)

        # Check for a collision with the border
        def check_if_collision_border(self):
            x_border = (self.length / 2 ) - 10
            y_border = (self.height / 2) - 10
            if self.head.xcor()>x_border or self.head.xcor()<-x_border or self.head.ycor()>y_border or self.head.ycor()<-y_border:
                time.sleep(1)
                self.head.goto(0,0)
                self.head.direction = "stop"
                self.hide_and_clear_segments()
                self.reset_score_and_delay()
                self.update_score_disp()

        # Check to see if the snake head is on the food location
        def check_if_got_food(self):
            if self.head.xcor() == self.food.xcor() and self.head.ycor() == self.food.ycor():
                self.move_food_random()
                self.add_segment()
                # Shorten the delay
                self.delay -= 0.001
                # Increase the Score
                self.score += 10
                # Increase the high_score
                if self.score > self.high_score:
                    self.high_score = self.score
                self.update_score_disp()

        # Move the head of the snake and the tail (if there is a tail)
        def move_the_snake(self):
            # Move the end segments first in reverse order
            for index in range(len(self.segments)-1,0,-1):
                x = self.segments[index-1].xcor()
                y = self.segments[index-1].ycor()
                self.segments[index].goto(x, y)
            # Move segment 0 to where the head is
            if len(self.segments) > 0:
                x = self.head.xcor()
                y = self.head.ycor()
                self.segments[0].goto(x,y)
            self.move()

        def check_if_collision_body(self):
            # Check for head Collision with the body segments
            for segment in self.segments:
                if segment.distance(self.head) < 20:
                    time.sleep(1)
                    self.head.goto(0,0)
                    self.head.direction = "stop"
                    self.hide_and_clear_segments()
                    self.reset_score_and_delay()
                    self.update_score_disp()
    """

    # Move the snake, and at any point if snake dead, break
    def move_snake(self):
        row_move,col_move = self.convert_direction_to_int()
        self.grid.snake_move(row_move,col_move)
        # We did not die.
        if not self.grid.isdead:
            # We ate food, so food went to a new location, we grew, and moved
            if self.grid.grew:
                x,y = self.convert_grid_to_coord(self.grid.food_location)
                self.food.goto(x, y)
                self.add_segment()
                # Shorten the delay
                self.delay -= 0.001
                # Increase the Score
                self.score += 10
                # Increase the high_score if higher
                if self.score > self.high_score:
                    self.high_score = self.score
                self.update_score_disp()

            # New snake head location
            x,y = self.convert_grid_to_coord(self.grid.head)
            self.head.goto(x,y)
            # New tail locations
            i = 0
            for body_node in self.grid.tail.get_queue():
                x,y = self.convert_grid_to_coord(body_node)
                self.segments[i].goto(x,y)
                i += 1
            #self.move()
        # We did die. Reset the location of the snake head. restart.
        else:
            self.grid.__init__(self.grid_height,self.grid_length)
            time.sleep(1)
            x,y = self.convert_grid_to_coord(self.grid.head)
            self.head.goto(x,y)
            x,y = self.convert_grid_to_coord(self.grid.food_location)
            self.food.goto(x,y)
            self.head.direction = "stop"
            self.hide_and_clear_segments()
            self.reset_score_and_delay()
            self.update_score_disp()

    # Takes the direction of the snake and converts it to int
    def convert_direction_to_int(self):
        x = 0
        y = 0
        if self.head.direction == "up":
            x = -1
        elif self.head.direction == "down":
            x = 1
        elif self.head.direction == "left":
            y = -1
        elif self.head.direction == "right":
            y = 1
        return [x,y]

    # Change the direction of the snake to up
    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    # Change the direction of the snake to down
    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    # Change the direction of the snake to left
    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    # Change the direction of the snake to right
    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move_food_random(self):
        # Move the food to random spot
        self.grid.spawn_food()
        x,y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)

    def print_grid(self):
        index = 0
        for element in self.grid.grid:
            print(element, end=' ')
            print(index)
            index += 1
        print()

gui = Gui(grid_length, grid_height,g)

# Main Game Loop
while True:
    gui.window.update()
    print(gui.head.direction)
    # move the snake through the grid.
    gui.move_snake()
    gui.print_grid()
    '''
    # Check for a collision with the border
    gui.check_if_collision_border()

    # Check for collision with food
    gui.check_if_got_food()

    # Move the snake around the grid
    gui.move_the_snake()

    # Check for head Collision with the body segments
    gui.check_if_collision_body()
    '''

    # Pause the execution of the program so it doesn't go lightning fast
    time.sleep(gui.delay)

gui.window.mainloop()
