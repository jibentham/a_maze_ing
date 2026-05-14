import random
from maze_gen import Cell, Grid
from dfs_backtracker import get_unvisited_neighbors, remove_wall, generate_recursive_backtracker


def generate_prims(grid):
    start = grid.cells[0][0]
    start.visited = True
    yield start

    # frontier: list of (direction, from_cell, to_cell)
    frontier = []

    def add_frontier(cell):
        row, col = cell.y, cell.x
        if row > 0:
            n = grid.cells[row - 1][col]
            if not n.visited:
                frontier.append(('N', cell, n))
        if row < grid.height - 1:
            n = grid.cells[row + 1][col]
            if not n.visited:
                frontier.append(('S', cell, n))
        if col < grid.width - 1:
            n = grid.cells[row][col + 1]
            if not n.visited:
                frontier.append(('E', cell, n))
        if col > 0:
            n = grid.cells[row][col - 1]
            if not n.visited:
                frontier.append(('W', cell, n))

    add_frontier(start)

    while frontier:
        direction, from_cell, to_cell = random.choice(frontier)
        frontier.remove((direction, from_cell, to_cell))

        if to_cell.visited:
            continue

        remove_wall(from_cell, to_cell, direction)
        to_cell.visited = True
        add_frontier(to_cell)
        yield to_cell