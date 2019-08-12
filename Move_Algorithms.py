import random
import copy
import queue
from math import floor
from my_stack import Stack
from my_queue import Queue


def go_up():
    return ["up"]  # [-1, 0]


def go_down():
    return ["down"]  # [1, 0]


def go_left():
    return ["left"]  # [0, -1]


def go_right():
    return ["right"]  # [0, 1]


MOVES = {
            "up": {
                "x": -1,
                "y": 0,
                "move": go_up
            },
            "down": {
                "x": 1,
                "y": 0,
                "move": go_down
            },
            "left": {
                "x": 0,
                "y": -1,
                "move": go_left
            },
            "right": {
                "x": 0,
                "y": 1,
                "move": go_right
            }
    }


class RandomPath:

    @staticmethod
    def random_direction(gui):
        # Get a random int, each option representing a direction: 0 = up, 1 = down, 2 = left, 3 = right
        rand_direction = random.randint(0, 3)
        move = None
        if rand_direction == 0:
            move = MOVES["up"]
        elif rand_direction == 1:
            move = MOVES["down"]
        elif rand_direction == 2:
            move = MOVES["left"]
        elif rand_direction == 3:
            move = MOVES["right"]

        # while our next move WILL kill our snake, we pick a new move to see if that move won't kill us
        while not gui.grid.snake_check_move(move["x"], move["y"]) and gui.recursive_count < gui.death_threshold:
            # if we try this too many times, there probably isn't a safe direction, so we force a move that will kill
            gui.recursive_count += 1
            rand_direction = random.randint(0, 3)
            if rand_direction == 0:
                move = MOVES["up"]
            elif rand_direction == 1:
                move = MOVES["down"]
            elif rand_direction == 2:
                move = MOVES["left"]
            elif rand_direction == 3:
                move = MOVES["right"]
        gui.recursive_count = 0
        return move["move"]()


class ShortestPath:

    @staticmethod
    def shortest_euclidean_direction(gui):
        # Make the largest distance huge, so no errors could possible happen ;)
        x1, y1 = gui.grid.head.get_node()
        closest = gui.length * gui.height
        closest_move = None
        # which direction would decrease the distance the most?
        for move in MOVES:
            temp_distance = food_distance(gui, x1 + MOVES[move]["x"], y1 + MOVES[move]["y"])
            if temp_distance < closest:
                closest = temp_distance
                closest_move = move
        # move the snake in the direction that would decrease the distance by the most amount
        return MOVES[closest_move]["move"]()

    @staticmethod
    def shortest_euclidean_direction_no_suicide(gui):
        move = MOVES[ShortestPath.shortest_euclidean_direction(gui)[0]]

        # While our next move kills the snake, pick a new move, so we don't kill snake
        while not gui.grid.snake_check_move(move["x"], move["y"]) and gui.recursive_count < gui.death_threshold:
            # if we try this too many times, there probably isn't a safe direction, so we force a move that will kill
            gui.recursive_count += 1
            rand_direction = random.randint(0, 3)
            if rand_direction == 0:
                move = MOVES["up"]
            elif rand_direction == 1:
                move = MOVES["down"]
            elif rand_direction == 2:
                move = MOVES["left"]
            elif rand_direction == 3:
                move = MOVES["right"]
        gui.recursive_count = 0
        return move["move"]()

    @staticmethod
    def shortest_euclidean_direction_farthest_path(gui):
        move = MOVES[ShortestPath.shortest_euclidean_direction(gui)[0]]

        # While our next move kills the snake, pick a new move, so we don't kill snake
        while not gui.grid.snake_check_move(move["x"], move["y"]) and gui.recursive_count < gui.death_threshold:
            # if we try this too many times, there probably isn't a safe direction, so we force a move that will kill
            gui.recursive_count += 1
            # choose the direction with the most amount of space for the head to travel. (max distance from head)
            move = MOVES[go_furthest(gui)[0]]
        gui.recursive_count = 0
        return move["move"]()

    @staticmethod
    def shortest_direction(gui):
        # get the location of the snake head
        snake_x, snake_y = gui.grid.head.get_node()
        # get the location of the food
        food_x, food_y = gui.grid.food_location.get_node()

        # based on direction, go to the food. Note: no suicide prevention and left/right comes before up/down
        if snake_y < food_y:
            return go_right()
        elif snake_y > food_y:
            return go_left()
        else:
            if snake_x < food_x:
                return go_down()
            elif snake_x > food_x:
                return go_up()

    @staticmethod
    def shortest_direction_no_suicide(gui):
        move = MOVES[ShortestPath.shortest_direction(gui)[0]]

        # While our next move kills the snake, pick a new move, so we don't kill snake
        while not gui.grid.snake_check_move(move["x"], move["y"]) and gui.recursive_count < gui.death_threshold:
            # if we try this too many times, there probably isn't a safe direction, so we force a move that will kill
            gui.recursive_count += 1
            rand_direction = random.randint(0, 3)
            if rand_direction == 0:
                move = MOVES["up"]
            elif rand_direction == 1:
                move = MOVES["down"]
            elif rand_direction == 2:
                move = MOVES["left"]
            elif rand_direction == 3:
                move = MOVES["right"]
        gui.recursive_count = 0
        return move["move"]()

    @staticmethod
    def shortest_direction_furthest_path(gui):
        # We updated the direction on the gui, but we want to check our move so we don't kill ourselves
        move = MOVES[ShortestPath.shortest_direction(gui)[0]]

        # While our next move kills the snake, pick a new move, so we don't kill snake
        while not gui.grid.snake_check_move(move["x"], move["y"]) and gui.recursive_count < gui.death_threshold:
            # if we try this too many times, there probably isn't a safe direction, so we force a move that will kill
            gui.recursive_count += 1
            # choose the direction with the most amount of space for the head to travel. (max distance from head)
            move = MOVES[go_furthest(gui)[0]]
        gui.recursive_count = 0
        return move["move"]()


class SmartPath:

    @staticmethod
    def smart_path(gui):
        move = MOVES[ShortestPath.shortest_euclidean_direction(gui)[0]]

        # Figure out which direction we are going
        direction = None
        # Direction = up = 0
        if move["x"] == -1:
            direction = 0
        # Direction = down = 1
        elif move["x"] == 1:
            direction = 1
        # Direction = left = 2
        elif move["y"] == -1:
            direction = 2
        # Direction = right = 3
        else:
            direction = 3

        if put_in_box(gui, direction):
            move = MOVES[go_furthest_no_box(gui)[0]]

        while not gui.grid.snake_check_move(move["x"], move["y"]) and gui.recursive_count < gui.death_threshold / 2:
            # if we try this too many times, there probably isn't a safe direction, so we force a move
            gui.recursive_count += 1
            # choose the direction with the most amount of space for the head to travel. (max distance from head)
            move = MOVES[go_furthest_no_box(gui)[0]]
        if gui.recursive_count > gui.death_threshold / 2:
            move = MOVES[go_furthest(gui)[0]]
        gui.recursive_count = 0
        return move["move"]()


class DepthFirstSearch:
    @staticmethod
    def dfs(gui, one_step=False):
        starting_pos = gui.grid.head.get_node()
        fringe = Stack()
        # Fringe holds a list of tuples: (node position, move to get prev to current, cost)
        fringe.push([(starting_pos, None, 0)])
        path = []
        visited = [starting_pos]
        while not fringe.is_empty():
            # Get the next one to be popped off the stack to search it's neighbor nodes (successors)
            path = fringe.pop()
            visited.append(path[-1][0])
            if gui.grid.grid[path[-1][0][0]][path[-1][0][1]] == 3:
                break

            for neighbor in get_neighbors(gui, path[-1][0][0], path[-1][0][1]):
                if neighbor[0] not in visited:
                    updated_path = copy.copy(path)
                    updated_path.append(neighbor)
                    fringe.push(updated_path)

        if not fringe.is_empty():
            move_set = []
            while path:
                temp = path.pop(0)
                if temp[1] is not None:
                    move_set.append(temp[1])
            if not one_step:
                return move_set
            else:
                return [move_set[0]]
        else:
            no_dfs_move = go_furthest(gui)
            if no_dfs_move:
                return no_dfs_move
            else:
                no_moves_at_all = go_down()
                return no_moves_at_all


class BreadthFirstSearch:
    @staticmethod
    def bfs(gui, one_step=False):
        starting_pos = gui.grid.head.get_node()
        fringe = Queue()
        # Fringe holds a list of tuples: (node position, move to get prev to current, cost)
        fringe.enqueue([(starting_pos, None, 0)])
        path = []
        visited = [starting_pos]
        while not fringe.is_empty():
            # Get the next one to be popped off the stack to search it's neighbor nodes (successors)
            path = fringe.dequeue()

            if gui.grid.grid[path[-1][0][0]][path[-1][0][1]] == 3:
                break

            for neighbor in get_neighbors(gui, path[-1][0][0], path[-1][0][1]):
                if neighbor[0] not in visited:
                    updated_path = copy.copy(path)
                    updated_path.append(neighbor)
                    fringe.enqueue(updated_path)
                    if not gui.grid.grid[neighbor[0][0]][neighbor[0][1]] == 3:
                        visited.append(neighbor[0])

        if not fringe.is_empty():
            move_set = []
            while path:
                temp = path.pop(0)
                if temp[1] is not None:
                    move_set.append(temp[1])
            if not one_step:
                return move_set
            else:
                return [move_set[0]]
        else:
            no_bfs_move = go_furthest(gui)
            if no_bfs_move:
                return no_bfs_move
            else:
                no_moves_at_all = go_down()
                return no_moves_at_all


class UniformCostSearch:
    @staticmethod
    def ucs(gui, one_step=False):
        starting_pos = gui.grid.head.get_node()
        fringe = queue.PriorityQueue()
        # Fringe holds a list of tuples: (node position, move to get prev to current, cost)
        fringe.put((0, [(starting_pos, None, 0)]))
        path = []
        visited = [starting_pos]
        while not fringe.empty():
            # Get the next one to be popped off the stack to search it's neighbor nodes (successors)
            path_object = fringe.get()
            path_cum_cost = path_object[0]
            path = path_object[1]

            if gui.grid.grid[path[-1][0][0]][path[-1][0][1]] == 3:
                break

            for neighbor in get_neighbors(gui, path[-1][0][0], path[-1][0][1]):
                if neighbor[0] not in visited:
                    updated_path = copy.copy(path)
                    updated_path.append(neighbor)
                    fringe.put((path_cum_cost + neighbor[2], updated_path))
                    if not gui.grid.grid[neighbor[0][0]][neighbor[0][1]] == 3:
                        visited.append(neighbor[0])

        if not fringe.empty():
            move_set = []
            while path:
                temp = path.pop(0)
                if temp[1] is not None:
                    move_set.append(temp[1])
            if not one_step:
                return move_set
            else:
                return [move_set[0]]
        else:
            no_ucs_move = go_furthest(gui)
            if no_ucs_move:
                return no_ucs_move
            else:
                no_moves_at_all = go_down()
                return no_moves_at_all


class AStarSearch:
    @staticmethod
    def astar(gui, one_step=False):
        starting_pos = gui.grid.head.get_node()
        fringe = queue.PriorityQueue()
        # Fringe holds a list of tuples: (node position, move to get prev to current, cost)
        fringe.put((heuristic(gui, starting_pos[0], starting_pos[1]), [(starting_pos, None, 0), 0]))
        path = []
        visited = [starting_pos]
        while not fringe.empty():
            # Get the next one to be popped off the stack to search it's neighbor nodes (successors)
            path_object = fringe.get()
            path = path_object[1]
            path_cum_cost = path.pop()

            if gui.grid.grid[path[-1][0][0]][path[-1][0][1]] == 3:
                break

            for neighbor in get_neighbors(gui, path[-1][0][0], path[-1][0][1]):
                if neighbor[0] not in visited:
                    updated_path = copy.copy(path)
                    updated_path.append(neighbor)
                    updated_cost = neighbor[2] + path_cum_cost
                    updated_path.append(updated_cost)
                    fringe.put((updated_path[-1] + heuristic(gui, neighbor[0][0], neighbor[0][1]), updated_path))
                    if not gui.grid.grid[neighbor[0][0]][neighbor[0][1]] == 3:
                        visited.append(neighbor[0])

        if not fringe.empty():
            move_set = []
            while path:
                temp = path.pop(0)
                if temp[1] is not None:
                    move_set.append(temp[1])
            if not one_step:
                return move_set
            else:
                return [move_set[0]]
        else:
            no_ucs_move = go_furthest(gui)
            if no_ucs_move:
                return no_ucs_move
            else:
                no_moves_at_all = go_down()
                return no_moves_at_all


# HELPER METHODS

# If the snake is surrounded, we want to choose the direction that has the furthest tail distance
def go_furthest(gui):
    snake_x, snake_y = gui.grid.head.get_node()
    # Check left Length
    i = 1
    while snake_y - i >= 0 and gui.grid.grid[snake_x][snake_y - i] != 2:
        i += 1
    # If there is not a tail to the left, then reward that path more.
    if snake_y - i < 0:
        i += 2
    # print('left = {}'.format(i))
    left = i
    # Check right Length
    i = 1
    while snake_y + i <= gui.grid.length - 1 and gui.grid.grid[snake_x][snake_y + i] != 2:
        i += 1
    # If there is not a tail to the right, then reward that path more.
    if snake_y + i > gui.grid.length - 1:
        i += 2
    # print('right = {}'.format(i))
    right = i
    # Check up Length
    i = 1
    while snake_x - i >= 0 and gui.grid.grid[snake_x - i][snake_y] != 2:
        i += 1
    # If there is not a tail to the up, then reward that path more.
    if snake_x - i < 0:
        i += 2
    # print('up = {}'.format(i))
    up = i
    # Check down Length
    i = 1
    # print('before down and i = {}, snake_x = {}, snake_x + i = {}, grid[snake_x ][snake_y] = {}'.format(i,snake_x,snake_x + i,self.grid.grid[snake_x][snake_y] ))
    while snake_x + i <= gui.grid.height - 1 and gui.grid.grid[snake_x + i][snake_y] != 2:
        i += 1
    # print('down and i = {}'.format(i))
    # i -= 1
    # print('i now = i - 1 : {}'.format(i))
    # print('snake_x + i = {} <= self.grid.height - 1 = {}'.format(snake_x + i,self.grid.height - 1))
    # print('grid[snake_x + i][snake_y] != 2 but also == {}'.format(self.grid.grid[snake_x + i][snake_y]))
    # If there is not a tail to the down, then reward that path more.
    if snake_x + i > gui.grid.height - 1:
        i += 2
    # print('down = {}'.format(i))
    down = i
    # If left length is the largest
    if left >= right and left >= down and left >= up:
        # print('surrounded and left is direction with the tail the farthest from head')
        return go_left()
    # If right length is the largest
    if right >= left and right >= down and right >= up:
        # print('surrounded and right is direction with the tail the farthest from head')
        return go_right()
    # If up length is the largest
    if up >= right and up >= down and up >= left:
        # print('surrounded and up is direction with the tail the farthest from head')
        return go_up()
    # If down length is the largest
    if down >= right and down >= left and down >= up:
        # print('surrounded and down is direction with the tail the farthest from head')
        return go_down()
    # Default if none were hit
    return go_down()


def get_neighbors(gui, head_x, head_y):
    neighbors = []
    temp_position = {
        "up": [head_x - 1, head_y],
        "down": [head_x + 1, head_y],
        "left": [head_x, head_y - 1],
        "right": [head_x, head_y + 1]
    }
    for pos in temp_position:
        temp_x, temp_y = temp_position[pos][0], temp_position[pos][1]
        # if it is within the borders of the game board
        if 0 <= temp_x < gui.grid_rows and 0 <= temp_y < gui.grid_cols:
            if gui.grid.grid[temp_x][temp_y] == 0 or gui.grid.grid[temp_x][temp_y] == 3:
                neighbors.append(([temp_x, temp_y], pos, get_cost(gui, temp_x, temp_y)))
    return neighbors


def get_cost(gui, pos_x, pos_y):
    cost = 0

    # Using euclidean distance from the food as the cost
    cost += floor(food_distance(gui, pos_x, pos_y))
    return cost


def heuristic(gui, pos_x, pos_y):
    cost = 0

    # maybe a heuristic for being next to your own body?
    neighbors = []
    temp_position = {
        "up": [pos_x - 1, pos_y],
        "down": [pos_x + 1, pos_y],
        "left": [pos_x, pos_y - 1],
        "right": [pos_x, pos_y + 1]
    }
    for pos in temp_position:
        temp_x, temp_y = temp_position[pos][0], temp_position[pos][1]
        # if it is within the borders of the game board
        if 0 <= temp_x < gui.grid_rows and 0 <= temp_y < gui.grid_cols:
            if gui.grid.grid[temp_x][temp_y] == 2:
                neighbors.append(([temp_x, temp_y], pos, get_cost(gui, temp_x, temp_y)))
    if len(neighbors) > 1:
        cost -= len(neighbors) * 2

    # Being against the border is both a bad and a good thing. We should still increase the cost at the border
    if pos_x == 0 or pos_y == 0 or pos_x == gui.grid_rows - 1 or pos_y == gui.grid_cols - 1:
        cost += 15

    return cost

# Return the Euclidean distance from head to food
def food_distance(gui, x1=None, y1=None):
    if not x1 and not y1:
        x1, y1 = gui.grid.head.get_node()
    x2, y2 = gui.grid.food_location.get_node()
    return ((x2-x1)**2 + (y2-y1)**2)**0.5


# Direction is up = 0, down = 1, left = 2, right = 3. We want to determine if that will put us in a box
# Returns true if the next move will put in box and false if not in box
def put_in_box(gui, direction):
    snake_row, snake_col = gui.grid.head.get_node()
    # 0 is for up
    if direction == 0:
        if gui.grid.snake_check_move(-1, 0):
            snake_row -= 1
        # Return True : This will put in box (cuz it's an illegal move)
        else:
            return True
    # 1 is for down
    elif direction == 1:
        if gui.grid.snake_check_move(1, 0):
            snake_row += 1
        # Return True : This will put in box (cuz it's an illegal move)
        else:
            return True
    # 2 is for Left
    elif direction == 2:
        if gui.grid.snake_check_move(0, -1):
            snake_col -= 1
        # Return True : This will put in box (cuz it's an illegal move)
        else:
            return True
    # 3 is for Right
    elif direction == 3:
        if gui.grid.snake_check_move(0, 1):
            snake_col += 1
        # Return True : This will put in box (cuz it's an illegal move)
        else:
            return True
    is_left = False
    is_right = False
    is_up = False
    is_down = False
    # Go Through all the tails and see if we will box our self in with the border and our tail.
    for node in gui.grid.tail.get_queue():
        node_row, node_col = node.get_node()
        # print('snake row, snake col: {},{}. tail row, tail col: {},{}'.format(snake_row, snake_col, node_row, node_col))
        # Tail is below the head and this is the first time that we learn this. Also we aren't at a border
        if (not is_down) and (snake_col == node_col and (snake_row < node_row or snake_row == gui.grid.height - 1)):
            is_down = True
        # Tail is above the head and this is the first time that we learn this. Also we aren't at a border
        if (not is_up) and (snake_col == node_col and (snake_row > node_row or snake_row == 0)):
            is_up = True
        # Tail is right of the head and this is the first time that we learn this. Also we aren't at a border
        if (not is_right) and (snake_row == node_row and (snake_col < node_col or snake_col == gui.grid.length - 1)):
            is_right = True
        # Tail is left of the head and this is the first time that we learn this. Also we aren't at a border
        if (not is_left) and (snake_row == node_row and (snake_col > node_col or snake_col == 0)):
            is_left = True
        # Return true if we are surrounded
        if is_up and is_down and is_left and is_right:
            return True
    # if we care about Up
    if direction == 0 and is_up and is_left and is_right:
        # print("thinks it shouldn't go up")
        return True
    # if we care about Down
    elif direction == 1 and is_down and is_left and is_right:
        # print("thinks it shouldn't go down")
        return True
    # if we care about Left
    elif direction == 2 and is_up and is_down and is_left:
        # print("thinks it shouldn't go left")
        return True
    # if we care about Right
    elif direction == 3 and is_up and is_down and is_right:
        # print("thinks it shouldn't go right")
        return True
    else:
        return False


# If the snake is surrounded, we want to choose the direction that has the furthest tail distance
# Also keeps track if any future move in given direction will cause a box in
# Will choose the further distance if it is twice as much as the distance for no box
# THIS IS NOT PERFECT! SOMETIMES MAKES ERRORS!
def go_furthest_no_box(gui):
    distance = food_distance(gui)
    # These will keep track of the if a direction will cause a box or not.
    right_boxed_biased = False
    left_boxed_biased = False
    up_boxed_biased = False
    down_boxed_biased = False
    right_boxed = False
    left_boxed = False
    up_boxed = False
    down_boxed = False
    snake_x, snake_y = gui.grid.head.get_node()
    # Check left Length
    i = 1
    while snake_y - i >= 0 and gui.grid.grid[snake_x][snake_y - i] != 2:
        i += 1
    if put_in_box(gui, 2):
        left_boxed = True
        if i > 5 or distance > 5:
            left_boxed_biased = True

    # If there is not a tail to the left, then reward that path more.
    if snake_y - i < 0:
        i += 1
    # print('left = {}'.format(i))
    left = i
    # Check right Length
    i = 1
    while snake_y + i <= gui.grid.length - 1 and gui.grid.grid[snake_x][snake_y + i] != 2:
        i += 1
    if put_in_box(gui, 3):
        right_boxed = True
        if i > 5 or distance > 5:
            right_boxed_biased = True
    # If there is not a tail to the right, then reward that path more.
    if snake_y + i > gui.grid.length - 1:
        i += 1
    # print('right = {}'.format(i))
    right = i
    # Check up Length
    i = 1
    while snake_x - i >= 0 and gui.grid.grid[snake_x - i][snake_y] != 2:
        i += 1
    if put_in_box(gui, 0):
        up_boxed = True
        if i > 5 or distance > 5:
            up_boxed_biased = True
    # If there is not a tail to the up, then reward that path more.
    if snake_x - i < 0:
        i += 1
    # print('up = {}'.format(i))
    up = i
    # Check down Length
    i = 1
    while snake_x + i <= gui.grid.height - 1 and gui.grid.grid[snake_x + i][snake_y] != 2:
        i += 1
    if put_in_box(gui, 1):
        down_boxed = True
        if i > 5 or distance > 5:
            down_boxed_biased = True
    # If there is not a tail to the down, then reward that path more.
    if snake_x + i > gui.grid.height - 1:
        i += 1
    # print('down = {}'.format(i))
    down = i
    # If left length is the largest and doesnt create a box
    if left > right and left > down and left > up and not left_boxed:
        # print('go_furthest_no_box_smart and left is direction with the tail the farthest from head1')
        return go_left()
    # If right length is the largest and doesnt create a box
    if right > left and right > down and right > up and not right_boxed:
        # print('go_furthest_no_box_smart and right is direction with the tail the farthest from head1')
        return go_right()
    # If up length is the largest and doesnt create a box
    if up > right and up > down and up > left and not up_boxed:
        # print('go_furthest_no_box_smart and up is direction with the tail the farthest from head1')
        return go_up()
    # If down length is the largest and doesnt create a box
    if down > right and down > left and down > up and not down_boxed:
        # print('go_furthest_no_box_smart and down is direction with the tail the farthest from head1')
        return go_down()

    # If left length is the largest and is objectively and safely closer to food
    if left > right and left > down and left > up and not left_boxed_biased:
        # print('go_furthest_no_box_smart and left is direction with the tail the farthest from head2')
        return go_left()
    # If right length is the largest and is objectively and safely closer to food
    if right > left and right > down and right > up and not right_boxed_biased:
        # print('go_furthest_no_box_smart and right is direction with the tail the farthest from head2')
        return go_right()
    # If up length is the largest and is objectively and safely closer to food
    if up > right and up > down and up > left and not up_boxed_biased:
        # print('go_furthest_no_box_smart and up is direction with the tail the farthest from head2')
        return go_up()
    # If down length is the largest and is objectively and safely closer to food
    if down > right and down > left and down > up and not down_boxed_biased:
        # print('go_furthest_no_box_smart and down is direction with the tail the farthest from head2')
        return go_down()

    # If left length is at least the largest and is pretty close to the food
    if left >= right and left >= down and left >= up and (not left_boxed or not left_boxed_biased):
        # print('go_furthest_no_box_smart and left is direction with the tail the farthest from head3')
        return go_left()
    # If right length is at least the largest and is pretty close to the food
    if right >= left and right >= down and right >= up and (not right_boxed or not right_boxed_biased):
        # print('go_furthest_no_box_smart and right is direction with the tail the farthest from head3')
        return go_right()
    # If up length is at least the largest and is pretty close to the food
    if up >= right and up >= down and up >= left and (not up_boxed or not up_boxed_biased):
        # print('go_furthest_no_box_smart and up is direction with the tail the farthest from head3')
        return go_up()
    # If down length is at least the largest and is pretty close to the food
    if down >= right and down >= left and down >= up and (not down_boxed or not down_boxed_biased):
        # print('go_furthest_no_box_smart and down is direction with the tail the farthest from head3')
        return go_down()
    # Default return
    return go_down()
