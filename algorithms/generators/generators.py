from algorithms.base import MazeGen
from algorithms.generators.dfs_backtracker import generate_recursive_backtracker
from algorithms.generators.prims import generate_prims


class DFSGen(MazeGen):
    def generate(self, grid):
        yield from generate_recursive_backtracker(grid)


class PrimsGen(MazeGen):
    def generate(self, grid):
        yield from generate_prims(grid)