from queue import PriorityQueue
from itertools import count
from maze.maze_gen import Grid

def heuristic(cell, grid):
    # estimate distance to goal using horizontal + vertical steps
    return abs(cell.y - grid.exit.y) + abs(cell.x - grid.exit.x)


def get_passable_neighbors(cell, grid):
    neighbors = []
    row = cell.y
    col = cell.x
    directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}

    for direction, (dy, dx) in directions.items():
        new_row, new_col = row + dy, col + dx
        if 0 <= new_row < grid.height and 0 <= new_col < grid.width:
            if not cell.walls[direction]:              # no wall = passable
                neighbors.append((grid.cells[new_row][new_col], direction))

    return neighbors


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:                        # walk backwards from goal to start
        current = came_from[current]
        path.insert(0, current)                        # build path in forward order
    return path


def astar_solve(grid):
    open_set = PriorityQueue()                         # cells to explore, cheapest first
    came_from = {}                                     # breadcrumb trail for path reconstruction
    g_score = {grid.entrance: 0}                         # actual cost to reach each cell
    f_score = {grid.entrance: heuristic(grid.entrance, grid)}  # g + estimated cost to goal
    counter = count() 
    open_set.put((f_score[grid.entrance], next(counter), grid.entrance)) # kick off from the start cell


    while not open_set.empty():
        _, __, current = open_set.get()                    # grab the most promising cell
        yield ('exploring', current)                   # animation hook

        if current == grid.exit:                        # reached the goal
            path = reconstruct_path(came_from, current)
            yield ('solution', path)                   # animation hook
            return path

        for neighbor, _ in get_passable_neighbors(current, grid):
            tentative_g = g_score[current] + 1        # cost to reach neighbor via current

            if tentative_g < g_score.get(neighbor, float('inf')):  # is this a better route?
                came_from[neighbor] = current          # record how we got here
                g_score[neighbor]   = tentative_g
                f_score[neighbor]   = tentative_g + heuristic(neighbor, grid)
                open_set.put((f_score[neighbor], next(counter), neighbor))  # add to frontier
