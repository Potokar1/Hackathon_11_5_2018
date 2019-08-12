from grid_for_ai import Grid
import turtle
import time
import Move_Algorithms as Move


class Gui:
    def __init__(self, grid_cols, grid_rows, grid):
        # Length and height (x,y) of the window. Each [row][col] in the grid is 20 pixels so mult our grid sizes by 20
        self.move_list = []
        self.length = grid_cols * 20
        self.height = grid_rows * 20
        self.grid_cols = grid_cols
        self.grid_rows = grid_rows
        self.frames = 100000
        self.got_food_score_change = -100
        self.died_score_change = 100000
        # Reference to the grid it came from
        self.grid = grid
        # Scores
        self.score = 0
        self.high_score = 0
        # Delay Timer so we don't go so fast!
        self.delay_start = 0
        # This is the seconds the game waits after death
        self.pause_delay = self.delay_start * 3 + 0.5
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
        # when recursive_count > death_threshold, then we kill snake. It has nowhere to go!
        self.death_threshold = 30
        self.recursive_count = 0
        self.bool_surrounded = False
        self.just_survived_count = 0

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
        self.window.setup(self.length + 200, self.height + 200)
        border = turtle.Turtle()
        border.speed(0)
        border.penup()
        border.setx(-self.length / 2 - 10)
        border.sety(-self.height / 2 + 10)
        border.pendown()
        border.forward(self.length)
        border.left(90)
        border.forward(self.height)
        border.left(90)
        border.forward(self.length)
        border.left(90)
        border.forward(self.height)
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
        # self.smart_direction()

        moves = {
            "up": [-1, 0],
            "down": [1, 0],
            "left": [0, -1],
            "right": [0, 1]
        }

        if not self.move_list:
            # Random Algorithm
            # self.move_list = Move.RandomPath.random_direction(gui=self)

            # Shortest path using euclidean distance, no suicide prevention
            # self.move_list = Move.ShortestPath.shortest_euclidean_direction(gui=self)

            # Shortest path using euclidean distance, suicide prevention is totally random
            # self.move_list = Move.ShortestPath.shortest_euclidean_direction_no_suicide(gui=self)

            # Shortest path using euclidean distance w/ suicide prevention. Goes direction with most amount of space
            # self.move_list = Move.ShortestPath.shortest_euclidean_direction_farthest_path(gui=self)

            # shortest path / straight route algorithm
            # self.move_list = Move.ShortestPath.shortest_direction(gui=self)

            # Shortest path w/ no kill self. note, suicide prevention is totally random
            # self.move_list = Move.ShortestPath.shortest_direction_no_suicide(gui=self)

            # Shortest path w/ suicide prevention. Goes in the direction with most amount of space
            # self.move_list = Move.ShortestPath.shortest_direction_furthest_path(gui=self)

            # longer path algorithm
            # self.move_list = Move.SmartPath.smart_path(gui=self)

            # Depth First Search
            # self.move_list = Move.DepthFirstSearch.dfs(gui=self)

            # Breadth First Search
            # self.move_list = Move.BreadthFirstSearch.bfs(gui=self)

            # Uniform Cost Search
            # self.move_list = Move.UniformCostSearch.ucs(gui=self, one_step=True)

            # A Star Search
            self.move_list = Move.AStarSearch.astar(gui=self, one_step=True)

        self.head.xdirection, self.head.ydirection = moves[self.move_list.pop(0)]

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
        # self.print_grid()
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
        self.bool_surrounded = False
        self.just_survived_count = 0
        self.hide_and_clear_segments()
        # self.reset_score_and_delay()
        self.update_score_disp()

    def move_food_random(self):
        # Move the food to random spot
        self.grid.spawn_food()
        x, y = self.convert_grid_to_coord(self.grid.food_location)
        self.food.goto(x, y)

    # Bool Array Is for up, down, left, right, if this is a legal move!
    # Won't let the head go to the border
    def choose_smart(self, worked):
        distance = self.food_distance()
        snake_x, snake_y = self.grid.head.get_node()
        food_x, food_y = self.grid.food_location.get_node()
        print('distance = {}'.format(distance))
        if snake_x < food_x and (not snake_x >= self.grid.height - 2 or distance <= 2) and worked[1] and not self.put_in_box(1):
            # print('choose smart says: go down, worked[1]: {}, put_in_box(1): {}'.format(worked[1],self.put_in_box(1)))
            self.go_down()
        elif snake_x > food_x and (not snake_x <= 1 or distance <= 2) and worked[0] and not self.put_in_box(0):
            # print('choose smart says: go up, worked[0]: {}, put_in_box(0): {}'.format(worked[0],self.put_in_box(0)))
            self.go_up()
        else:
            if snake_y < food_y and (not snake_y >= self.grid.length - 2 or distance <= 2) and worked[3] and not self.put_in_box(3):
                # print('choose smart says: go right, worked[3]: {}, put_in_box(3): {}'.format(worked[3],self.put_in_box(3)))
                self.go_right()
            elif snake_y > food_y and (not snake_y <= 1 or distance <= 2) and worked[2] and not self.put_in_box(2):
                # print('choose smart says: go left, worked[2]: {}, put_in_box(2): {}'.format(worked[2],self.put_in_box(2)))
                self.go_left()
            else:
                self.just_survived_count += 1
                self.just_survive()

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
            if not is_down and (snake_y == node_y and (snake_x < node_x or snake_x == self.grid.height - 1)):
                print('surrounded: there is a tail down at {}'.format(node.get_node()))
                is_down = True
            # Tail is above the head and this is the first time that we learn this. Also we arn't at a border
            if not is_up and (snake_y == node_y and (snake_x > node_x or snake_x == 0)):
                print('surrounded: there is a tail up at {}'.format(node.get_node()))
                is_up = True
            # Tail is right of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_right and (snake_x == node_x and (snake_y < node_y or snake_y == self.grid.length - 1)):
                print('surrounded: there is a tail right at {}'.format(node.get_node()))
                is_right = True
            # Tail is left of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_left and (snake_x == node_x and (snake_y > node_y or snake_y == 0)):
                print('surrounded: there is a tail left at {}'.format(node.get_node()))
                is_left = True
            # Return true if we are surrounded
            if is_up and is_down and is_left and is_right:
                return True
        if not is_left:
            self.go_left()
            print('surrounded: we chose left. {},{} as move'.format(self.head.xdirection, self.head.ydirection))
        elif not is_up:
            self.go_up()
            print('surrounded: we chose up. {},{} as move'.format(self.head.xdirection, self.head.ydirection))
        elif not is_right:
            self.go_right()
            print('surrounded: we chose right. {},{} as move'.format(self.head.xdirection, self.head.ydirection))
        elif not is_down:
            self.go_down()
            print('surrounded: we chose down. {},{} as move'.format(self.head.xdirection, self.head.ydirection))
        # Return false if we are not surrounded
        return False

    # Returns True if we are surrounded by the tail,
    # Retrns False if there is a way out.
    # When Returned with False, Then current x/y direction will be safe
    def is_surrounded(self):   # THIS PART IS BUGGY!
        snake_x, snake_y = self.grid.head.get_node()
        is_left = False
        is_right = False
        is_up = False
        is_down = False
        for node in self.grid.tail.get_queue():
            node_x, node_y = node.get_node()
            # Tail is below the head and this is the first time that we learn this. Also we arn't at a border
            if not is_down and (snake_y == node_y and (snake_x < node_x or snake_x == self.grid_rows - 1)):
                # print('there is a tail down at {}'.format(node.get_node()))
                is_down = True
            # Tail is above the head and this is the first time that we learn this. Also we arn't at a border
            if not is_up and (snake_y == node_y and (snake_x > node_x or snake_x == 0)):
                # print('there is a tail up at {}'.format(node.get_node()))
                is_up = True
            # Tail is right of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_right and (snake_x == node_x and (snake_y < node_y or snake_y == self.grid_cols - 1)):
                # print('there is a tail right at {}'.format(node.get_node()))
                is_right = True
            # Tail is left of the head and this is the first time that we learn this. Also we arn't at a border
            if not is_left and (snake_x == node_x and (snake_y > node_y or snake_y == 0)):
                # print('there is a tail left at {}'.format(node.get_node()))
                is_left = True
            # Return true if we are surrounded
            if is_up and is_down and is_left and is_right:
                return True
        if is_up and is_left and is_right and is_down:
            return True
        else:
            # Return false if we are not surrounded
            return False

    # If the snake is surrounded, we want to choose the direction that has the furthest tail distance
    # Also keeps track if any future move in given direction will cause a box in
    def go_furthest_no_box(self):
        snake_x, snake_y = self.grid.head.get_node()
        # Check left Length
        i = 1
        while snake_y - i >= 0 and self.grid.grid[snake_x][snake_y - i] != 2 and not self.put_in_box(2):
            i += 1
        # If there is not a tail to the left, then reward that path more.
        if snake_y - i < 0:
            i += 2
        print('left = {}'.format(i))
        left = i
        # Check right Length
        i = 1
        while snake_y + i <= self.grid.length - 1 and self.grid.grid[snake_x][snake_y + i] != 2 and not self.put_in_box(3):
            i += 1
        # If there is not a tail to the right, then reward that path more.
        if snake_y + i > self.grid.length - 1:
            i += 2
        print('right = {}'.format(i))
        right = i
        # Check up Length
        i = 1
        while snake_x - i >= 0 and self.grid.grid[snake_x - i][snake_y] != 2 and not self.put_in_box(0):
            i += 1
        # If there is not a tail to the up, then reward that path more.
        if snake_x - i < 0:
            i += 2
        print('up = {}'.format(i))
        up = i
        # Check down Length
        i = 1
        # print('before down w/ box and i = {}, snake_x = {}, snake_x + i = {}, grid[snake_x][snake_y] = {}'.format(i,snake_x,snake_x + i,self.grid.grid[snake_x][snake_y] ))
        while snake_x + i <= self.grid.height - 1 and self.grid.grid[snake_x + i][snake_y] != 2 and not self.put_in_box(1):
            i += 1
        # print('down and i = {}'.format(i))
        # i -= 1
        # print('i now = i - 1 : {}'.format(i))
        # print('snake_x + i = {} <= self.grid.height - 1 = {}'.format(snake_x + i,self.grid.height - 1))
        # print('grid[snake_x + i][snake_y] != 2 but also == {}'.format(self.grid.grid[snake_x + i][snake_y]))
        # If there is not a tail to the down, then reward that path more.
        if snake_x + i > self.grid.height - 1:
            i += 2
        print('down = {}'.format(i))
        down = i
        # If left length is the largest
        if left >= right and left >= down and left >= up:
            print('go_furthest_no_box and left is direction with the tail the farthest from head')
            self.go_left()
            return
        # If right length is the largest
        if right >= left and right >= down and right >= up:
            print('go_furthest_no_box and right is direction with the tail the farthest from head')
            self.go_right()
            return
        # If up length is the largest
        if up >= right and up >= down and up >= left:
            print('go_furthest_no_box and up is direction with the tail the farthest from head')
            self.go_up()
            return
        # If down length is the largest
        if down >= right and down >= left and down >= up:
            print('go_furthest_no_box and down is direction with the tail the farthest from head')
            self.go_down()
            return

    # We want the snake to go up down or left right, not spiral to death.
    def just_survive(self):
        # ERROR WITH GOING TO CIRCLES. FRICKIN LOOPS
        self.go_furthest_no_box_smart()


    def smart_direction(self, worked=[True, True, True, True]):
        #print('increasing recursive count to {}'.format(self.recursive_count))
        self.recursive_count += 1
        if (not self.bool_surrounded and self.recursive_count <= 10) or self.just_survived_count > 5:
            self.choose_smart(worked)
        else:
            if self.is_surrounded():
                self.bool_surrounded = True
                self.just_survived_count += 1
                self.just_survive()
            else:
                self.just_survived_count = 0
                self.bool_surrounded = False
        row_move = self.head.xdirection
        col_move = self.head.ydirection
        while not self.grid.snake_check_move(row_move, col_move):
            #print('stuck here with {},{}'.format(self.head.xdirection, self.head.ydirection))
            if row_move == col_move and self.recursive_count >= 20:
                self.die()
            if self.surrounded():
                self.bool_surrounded = True
                #print('increasing recursive count to {}'.format(self.recursive_count))
                self.recursive_count += 1
                print('is surrounded')
                if self.just_survived_count < 10:
                    self.just_survived_count += 1
                    self.just_survive()
                else:
                    # THIS IS THE LAST THING I NEED TO DO
                    # CHANGE HOW RANDOM DISISIONS ARE DONE WHEN NOTHING LOOKS LIKE A GOOD MOVE
                    # HINT: PROBABLY NEEDS TO GO TO THE SIDE WITH THE FURTHEST TAIL DISTANCE
                    # AKA DONT MOVE TO THE SIDE WITH THE TAIL THAT IS ONE BLOCK AWAY BUT THE ONE
                    # THAT IS A COUPLE SPACES AWAY. GIVES MORE BREATHING ROOM
                    self.go_furthest()
            else:
                self.bool_surrounded = False
                self.just_survived_count = 0
            row_move = self.head.xdirection
            col_move = self.head.ydirection
            # print('try {},{}'.format(self.head.xdirection, self.head.ydirection))
            # For redundancy purposes
            row_move = self.head.xdirection
            col_move = self.head.ydirection

    def print_grid(self):
        index = 0
        for element in self.grid.grid:
            print(element, end=' ')
            print(index)
            index += 1
        print()

    def print_grid_with_costs(self):
        index = 0
        for x_pos in range(self.grid_rows):
            for y_pos in range(self.grid_cols):
                cost = Move.get_cost(gui, x_pos, y_pos)
                print("{:02d}".format(cost), end=" ")
                # print(Move.get_cost(self, element[0], element[1]), end=' ')
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
    # gui.print_grid()
    # gui.print_grid_with_costs()
    # move the snake through the grid.
    gui.move_snake()

    # Pause the execution of the program so it doesn't go lightning fast
    time.sleep(gui.delay)

gui.window.mainloop()
