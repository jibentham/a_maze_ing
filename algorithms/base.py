from abc import ABC, abstractmethod


class MazeGen(ABC):
    @abstractmethod
    def generate(self, grid):
        ...


class MazeSolve:
    @abstractmethod
    def solve(self, grid):
        ...


class MazeRender(ABC):
    @abstractmethod
    def render(self, grid, exploring=None, path=None):
        ...
