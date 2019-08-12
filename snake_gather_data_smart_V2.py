from grid_for_ai import Grid
from queue import Queue
import user_input as ui
import turtle
import time
import random


class Data():
    def __init__(self, grid_cols, grid_rows, grid):

        # STUFF FOR THE SNAKE
        self.iterations = 10000
        self.got_food_score_change = -100
        self.died_score_change = 100000
        self.recursive_count = 0
        self.xdirection = 0
        self.ydirection = 0
        self.set_snake_head()
        self.recursive_count = 0


        # STUFF FOR THE Game
        # Reference to the grid it came from
        self.grid = grid
        # Length and height (x,y) of the window. Each [row][col] in the grid is 20 pixels so we mult our grid sizes by 20
        self.grid_cols = grid_cols
        self.grid_rows = grid_rows


        # SNAKE METRICS FOR ANALYSIS
        self.score = 0
        self.score_data_dynamic = []
        self.score_data_dynamic_string = ''
        self.score_final = 0
        self.high_score = 0
        self.move_data = []
        self.move_data_string = ''
        self.grid_data = []
        self.grid_data_string = ''
        self.snake_head_data = []
        self.food_data = []

    # Sets up the Snake head. Places it in the center of the grid.
    def set_snake_head(self):
        self.xdirection = 0
        self.ydirection = 0

    # Move the snake, and at any point if snake dead, break
    def move_snake(self):
        self.smart_direction()
        self.recursive_count = 0
        row_move = self.xdirection
        col_move = self.ydirection
        self.grid.snake_move(row_move, col_move)
        # We did not die.
        if not self.grid.isdead:
            # We ate food, so food went to a new location, we grew, and moved
            if self.grid.grew:
                self.eat_and_grow()
        # We did die. Reset the location of the snake head. restart.
        else:
            self.die()

    # This is what happens when we ate food! Yummy!
    def eat_and_grow(self):
        # Change the Score for getting an apple
        self.score += self.got_food_score_change

    # This is what happens when a snake dies.
    def die(self):
        self.score += self.died_score_change
        self.recursive_count = 0
        self.grid.__init__(self.grid_rows, self.grid_cols)
        self.xdirection = 0
        self.ydirection = 0

    # Change the direction of the snake to up
    def go_up(self):
        if self.recursive_count > 50:
            self.die()
        elif self.xdirection == 1:
            # Try Again
            self.xdirection = 0
            self.ydirection = 0
            self.random_direction()
        else:
            self.xdirection = -1
            self.ydirection = 0

    # Change the direction of the snake to down
    def go_down(self):
        if self.recursive_count > 50:
            self.die()
        elif self.xdirection == -1:
            # Try Again
            self.xdirection = 0
            self.ydirection = 0
            self.random_direction()
        else:
            self.xdirection = 1
            self.ydirection = 0

    # Change the direction of the snake to left
    def go_left(self):
        if self.recursive_count > 50:
            self.die()
        elif self.ydirection == 1:
            # Try Again
            self.xdirection = 0
            self.ydirection = 0
            self.random_direction()
        else:
            self.xdirection = 0
            self.ydirection = -1

    # Change the direction of the snake to right
    def go_right(self):
        if self.recursive_count > 50:
            self.die()
        elif self.ydirection == -1:
            # Try Again
            self.xdirection = 0
            self.ydirection = 0
            self.random_direction()
        else:
            self.xdirection = 0
            self.ydirection = 1

    def move_food_random(self):
        # Move the food to random spot
        self.grid.spawn_food()

    # Chooses the fastest way to the food
    def choose_fastest(self):
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
            return True
        # if we care about Down
        elif direction == 1 and is_down and is_left and is_right:
            return True
        # if we care about Left
        elif direction == 2 and is_up and is_down and is_left:
            return True
        # if we care about Right
        elif direction == 3 and is_up and is_down and is_right:
            return True
        else:
            return False

    def choose_fastest_backward(self):
        snake_x, snake_y = self.grid.head.get_node()
        food_x, food_y = self.grid.food_location.get_node()

        if snake_y < food_y:
            self.go_right()
        elif snake_y > food_y:
            self.go_left()
        else:
            if snake_x < food_x:
                self.go_down()
            elif snake_x > food_x:
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
        if not is_left:
            self.go_left()
        elif not is_up:
            self.go_up()
        elif not is_right:
            self.go_right()
        elif not is_down:
            self.go_down()
        # Return false if we are not surrounded
        return False

    def smart_direction(self):
        # First we set our direction to the fastest route posible.
        coin_flip = random.randint(0, 1)
        self.choose_fastest() if coin_flip == 0
        self.choose_smart_backward() if coin_flip == 1
        row_move = self.xdirection
        col_move = self.ydirection

        # First we check to see if that direciton is legal
        # If it is illegal, then we will try to go
        if not self.grid.snake_check_move(row_move,col_move):
            # We know the move is not legal, but we can still move!
            # Go in the direction that will get us

        # Then we check to see if that direction is actually optimal


        while not self.grid.snake_check_move(row_move, col_move):
            if row_move == col_move and self.recursive_count >= 30:
                self.die()
            if self.surrounded():
                self.recursive_count += 1
                rand_direction = random.randint(0, 3)
                if rand_direction == 0:
                    self.go_up()
                elif rand_direction == 1:
                    self.go_down()
                elif rand_direction == 2:
                    self.go_left()
                elif rand_direction == 3:
                    self.go_right()
            row_move = self.xdirection
            col_move = self.ydirection
            # For redundancy purposes
            row_move = self.xdirection
            col_move = self.ydirection

    def print_grid(self):
        index = 0
        for element in self.grid.grid:
            print(element, end=' ')
            print(index)
            index += 1
        print()

    # Collects the state of the grid and create a single list of the entire game.
    def get_grid_data_single(self):
        for element in self.grid.grid:
            self.grid_data.extend(element)

    # Collects the state of the grid and create a single list of the entire game.
    def get_grid_data_string(self):
        for element in self.grid.grid:
            for value in element:
                self.grid_data_string += str(value)

    # Collects the state of the grid and appends each row into the list. list of rows
    def get_grid_data_rows(self):
        for element in self.grid.grid:
            self.grid_data.append(element)

    # Collects the state of the grid and appends The grid into the list. list of grids (list of rows (list of cols))
    def get_grid_data_grids(self):
        self.grid_data.append(self.grid.grid)

    # Collects the state of the current score, puts every score update in a list
    def get_score_data_dynamic(self):
        self.score_data_dynamic.append(self.score)

    # Collects the state of the current score, puts every score update in a list
    def get_score_data_dynamic_string(self):
        self.score_data_dynamic_string += str(self.score)
        self.score_data_dynamic_string += ' '

    # Collects the staet of the current move, puts every move into a list. pretty for petty human eyes
    def get_move_data_for_humans(self):
        self.move_data.append([self.xdirection, self.ydirection])

    # Collects the staet of the current move, puts every move into a list. pretty for petty human eyes
    def get_move_data_for_humans_string(self):
        self.move_data_string += '('
        self.move_data_string += str(self.xdirection)
        self.move_data_string += ','
        self.move_data_string += str(self.ydirection)
        self.move_data_string += ')'
        self.move_data_string += ' '

    # Collects the staet of the current move, puts every move into a list.
    def get_move_data(self):
        self.move_data.append(self.xdirection)
        self.move_data.append(self.ydirection)

    # Collects the staet of the current move, puts every move into a list.
    def get_move_data_string(self):
        self.move_data_string += str(self.xdirection)
        self.move_data_string += str(self.ydirection)
        self.move_data_string += ' '

    # Store the position in the 2D array of where the snake head is at current turn.
    def get_snake_head_location(self):
        self.snake_head_data.append(self.grid.head.get_node())

    # Store the position in the 2D array of where the snake head is at current turn.
    def get_food_location(self):
        self.food_data.append(self.grid.food_location.get_node())

    # Put the specified data collected in a sequential order for easy to read data for each move.
    # List of List of frames or iterations. First collects the grid size in rows and cols, Then the
    # Snake Head Location, Food Location,(move executes) Move it did, then score, then final score
    # Note: Make sure that these are in the correct order in the run function below!
    def pretty_compiled(self):
        compiled = []
        compiled.append([self.grid_rows, self.grid_cols])
        for index in range(len(self.snake_head_data)):
            # Looks like: [row,col]
            compiled.append(self.snake_head_data[index])
            # Looks like: [row,col]
            compiled.append(self.food_data[index])
            # Looks like: [row + or 1 or 0,col + or 1 or 0]
            compiled.append(self.move_data[index])
            # Looks like: #### (simply the score)
            compiled.append(self.score_data_dynamic[index])
        # Final score because calculated at end of iterations
        compiled.append(self.score)
        # So we know we reached the end of this runthrough
        compiled.append('!')
        return compiled


# This is like the main routine.
# Put data collection functions inside the for loop for data every frame.
# Put data collection functions outside the for loop for data at the very end.
def run(output_file):
    # row and col size of our board
    grid_rows = 5 * random.randint(1, 20)
    grid_cols = 5 * random.randint(1, 20)

    # Create Grid, Initialize Snake head, Spawn Food
    # ReLuuus - possible ai thing to look up and use
    g = Grid(grid_rows, grid_cols)

    data = Data(grid_cols, grid_rows, g)

    # Main Game Loop. Runs for a total number of iterations
    for _ in range(data.iterations):
        data.score += 1
        data.get_snake_head_location()
        data.get_food_location()
        # move the snake through the grid.
        data.move_snake()
        data.get_move_data_for_humans()
        data.get_score_data_dynamic()

    # Json file for the compiled data
    import json
    json.dump(data.pretty_compiled(), output_file)

    # output_file.write(data.move_data_string)
    # output_file.write(data.score_data_dynamic_string)
    ''' Json file printing to a file.
    import json
    # start with the grid rows and cols to be displayed for each iteration
    json.dump(grid_rows, output_file)
    json.dump(',', output_file)
    json.dump(grid_cols, output_file)
    json.dump(' ', output_file)
    # add in the move data for each iteration
    json.dump(data.move_data, output_file)
    json.dump(' ', output_file)
    # add in the score data for each iteration
    json.dump(data.score_data_dynamic, output_file)
    # Seperate iterations with a ! character
    json.dump('!', output_file)
    '''
