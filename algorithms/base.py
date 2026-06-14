from abc import ABC, abstractmethod


class MazeGenerator(ABC):
    def _remove_wall(self, cell_1, cell_2, direction):
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        cell_1.walls[direction] = False
        cell_2.walls[opposite[direction]] = False

    @abstractmethod
    def generate(self, grid):
        ...


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, grid):
        ...


class MazeRenderer(ABC):
    @abstractmethod
    def render(self, grid, exploring=None, path=None):
        ...
