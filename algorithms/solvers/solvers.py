from algorithms.base import MazeSolve
from algorithms.solvers.astar import astar_solve

class AStarSolve(MazeSolve):
    def solve(self, grid):
        yield from astar_solve(grid)