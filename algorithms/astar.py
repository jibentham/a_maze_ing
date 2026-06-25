from __future__ import annotations
from typing import Generator, Union
from queue import PriorityQueue
from itertools import count
from algorithms.base import MazeSolver
from maze.maze_gen import Cell, Grid


class AStarSolver(MazeSolver):
    def solve(
        self, grid: Grid
    ) -> Generator[
            Union[tuple[str, Cell]
                  | tuple[str, list[Cell], dict[Cell, Cell]]], None, None
            ]:
        assert grid.entrance is not None
        assert grid.exit is not None
        open_set: PriorityQueue[tuple[int, int, Cell]] = PriorityQueue()                         # cells to explore, cheapest first
        came_from: dict[Cell, Cell] = {}                                     # breadcrumb trail for path reconstruction
        g_score: dict[Cell, int] = {grid.entrance: 0}                         # actual cost to reach each cell
        f_score: dict[Cell, int] = {grid.entrance: self._heuristic(grid.entrance, grid)}  # g + estimated cost to goal
        counter = count()

        open_set.put((f_score[grid.entrance], next(counter), grid.entrance))  # kick off from the start cell
        while not open_set.empty():
            _, __, current = open_set.get()                    # grab the most promising cell
            yield ('exploring', current)                   # animation hook
            if current == grid.exit:                        # reached the goal
                path: list[Cell] = self._reconstruct_path(came_from, current)
                yield ('solution', path, came_from)                   # animation hook
                return
            for neighbor, _ in self._get_passable_neighbors(current, grid):
                tentative_g: int = g_score[current] + 1        # cost to reach neighbor via current
                if tentative_g < g_score.get(neighbor, float('inf')):  # is this a better route?
                    came_from[neighbor] = current          # record how we got here
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, grid)
                    open_set.put((f_score[neighbor], next(counter), neighbor))  # add to frontier

    def _heuristic(self, cell: Cell, grid: Grid) -> int:
        assert grid.exit is not None
        # estimate distance to goal using horizontal + vertical steps
        return abs(cell.y - grid.exit.y) + abs(cell.x - grid.exit.x)

    def _get_passable_neighbors(
        self, cell: Cell, grid: Grid
    ) -> list[tuple[Cell, str]]:
        neighbors: list[tuple[Cell, str]] = []
        row: int = cell.y
        col: int = cell.x
        directions: dict[str, tuple[int, int]] = {
            'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)
        }

        for direction, (dy, dx) in directions.items():
            new_row: int = row + dy
            new_col: int = col + dx
            if 0 <= new_row < grid.height and 0 <= new_col < grid.width:
                if not cell.walls[direction]:              # no wall = passable
                    neighbors.append((grid.cells[new_row][new_col], direction))
        return neighbors

    def _reconstruct_path(
        self, came_from: dict[Cell, Cell], current: Cell
    ) -> list[Cell]:
        path: list[Cell] = [current]

        while current in came_from:                        # walk backwards from goal to start
            current = came_from[current]
            path.insert(0, current)                        # build path in forward order
        return path
