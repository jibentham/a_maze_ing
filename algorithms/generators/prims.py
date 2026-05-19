import random
from maze.maze_gen import Grid
from maze.maze_gen_utils import is_sealed
from algorithms.generators.dfs_backtracker import remove_wall


def generate_prims(grid):
    start = grid.cells[0][0]
    start.visited = True
    yield start

    frontier = []

    def add_frontier(cell):
        row, col = cell.y, cell.x
        if row > 0:
            n = grid.cells[row - 1][col]
            if not n.visited and not is_sealed(n):
                frontier.append(('N', cell, n))
        if row < grid.height - 1:
            n = grid.cells[row + 1][col]
            if not n.visited and not is_sealed(n):
                frontier.append(('S', cell, n))
        if col < grid.width - 1:
            n = grid.cells[row][col + 1]
            if not n.visited and not is_sealed(n):
                frontier.append(('E', cell, n))
        if col > 0:
            n = grid.cells[row][col - 1]
            if not n.visited and not is_sealed(n):
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