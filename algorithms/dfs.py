import random
from maze.maze_gen_utils import is_sealed
from algorithms.base import MazeGenerator


class DFSGenerator(MazeGenerator):
    def generate(self, grid):
        stack = []
        current = grid.cell_list[0]

        yield current

        while True:
            neighbors = self._get_unvisited_neighbors(current, grid)

            if neighbors:
                direction, chosen = random.choice(neighbors)
                stack.append(current)
                self._remove_wall(current, chosen, direction)
                current = chosen
                current.visited = True
                yield current                   # animation hook: moved forward

            elif stack:
                current = stack.pop()
                yield current                   # animation hook: backtracking

            else:
                break                           # stack empty every cell visited

    def _get_unvisited_neighbors(self, cell, grid):
        neighbors = []
        row, col = cell.y, cell.x
        if row > 0:
            n = grid.cells[row - 1][col]
            if not n.visited and not is_sealed(n):
                neighbors.append(('N', n))
        if row < grid.height - 1:
            n = grid.cells[row + 1][col]
            if not n.visited and not is_sealed(n):
                neighbors.append(('S', n))
        if col < grid.width - 1:
            n = grid.cells[row][col + 1]
            if not n.visited and not is_sealed(n):
                neighbors.append(('E', n))
        if col > 0:
            n = grid.cells[row][col - 1]
            if not n.visited and not is_sealed(n):
                neighbors.append(('W', n))
        return neighbors
