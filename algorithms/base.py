from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generator, Iterator, Optional, Union
from maze.maze_gen import Cell, Grid


class MazeGenerator(ABC):
    def _remove_wall(self, cell_1: Cell, cell_2: Cell, direction: str) -> None:
        opposite: dict[str, str] = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        cell_1.walls[direction] = False
        cell_2.walls[opposite[direction]] = False

    @abstractmethod
    def generate(self, grid: Grid) -> Iterator[Cell]:
        ...


class MazeSolver(ABC):
    @abstractmethod
    def solve(
        self, grid: Grid
    ) -> Generator[Union[tuple[str, Cell], tuple[str, list[Cell], dict[Cell, Cell]]], None, None]:
        ...


class MazeRenderer(ABC):
    @abstractmethod
    def render(
            self,
            grid: Grid,
            exploring: Optional[tuple[int, int]]=None,
            path: Optional[set[tuple[int, int]]]=None
    ) -> None:
        ...
