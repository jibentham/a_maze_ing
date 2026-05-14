import random
from maze_gen import Cell, Grid

def get_unvisited_neighbors(cell, grid):
    neighbors = []
    row = cell.y # y = vertical
    col = cell.x # x is horizontal

    # North: row above is there and is unvisited
    if row > 0:                         # is there a cell above
        n = grid.cells[row - 1][col]    # grab it
        if not n.visited:
            neighbors.append(('N', n))

    # South: row below is there and is unvisited
    if row < grid.height - 1:
        n = grid.cells[row + 1][col]
        if not n.visited:
            neighbors.append(('S', n))

    # East: column to the right exists and is unvisited
    if col < grid.width - 1:
        n = grid.cells[row][col + 1]
        if not n.visited:
            neighbors.append(('E', n))

    # West: column to the left exists and is unvisited
    if col > 0:
        n = grid.cells[row][col - 1]
        if not n.visited:
            neighbors.append(('W', n))
    
    return neighbors


def remove_wall(cell1, cell2, direction):
    opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    cell1.walls[direction] = False
    cell2.walls[opposite[direction]] = False


def generate_recursive_backtracker(grid):
    stack = []
    current = grid.cell_list[0]

    yield current

    while True:
        neighbors = get_unvisited_neighbors(current, grid)

        if neighbors:
            direction, chosen = random.choice(neighbors)
            stack.append(current)
            remove_wall(current, chosen, direction)
            current = chosen
            current.visited = True
            yield current                   # animation hook: moved forward

        elif stack:
            current = stack.pop()
            yield current                   # animation hook: backtracking

        else:
            break                           # stack empty every cell visited