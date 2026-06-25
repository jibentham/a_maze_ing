from __future__ import annotations
import random
from typing import Iterator
from maze.maze_gen import Cell, Grid
from maze.maze_gen_utils import is_sealed
from algorithms.base import MazeGenerator


class PrimsGenerator(MazeGenerator):
    def generate(self, grid: Grid) -> Iterator[Cell]:
        start: Cell = grid.cells[0][0]
        start.visited = True
        yield start

        frontier: list[tuple[str, Cell, Cell]] = []
        self._add_frontier(start, grid, frontier)

        while frontier:
            direction: str
            from_cell: Cell
            to_cell: Cell
            direction, from_cell, to_cell = random.choice(frontier)
            frontier.remove((direction, from_cell, to_cell))

            if to_cell.visited:
                continue

            self._remove_wall(from_cell, to_cell, direction)
            to_cell.visited = True
            self._add_frontier(to_cell, grid, frontier)
            yield to_cell

    def _add_frontier(
        self, cell: Cell, grid: Grid, frontier: list[tuple[str, Cell, Cell]]
    ) -> None:
        row: int = cell.y
        col: int = cell.x
        if row > 0:
            n: Cell = grid.cells[row - 1][col]
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
