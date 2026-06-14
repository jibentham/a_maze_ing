import os
import random
from maze.maze_gen import Grid
from maze.maze_gen_utils import add_loops, brand_maze, reseal_brand
from algorithms import get_generator, get_solver, get_renderer
from config import Config


class MazeRunner:
    def __init__(self, config):
        self.config    = config
        self.grid      = None
        self.generator = get_generator(config.generator)
        self.solver    = get_solver(config.solver)
        self.renderer  = get_renderer('ascii', config.colors)

    def build(self):
        cfg = self.config
        self.grid = Grid(cfg.width, cfg.height)
        self.grid.populate_grid()
        self.grid.set_entrance(*cfg.entrance)
        self.grid.set_exit(*cfg.exit)

        brand_maze(self.grid)              # mark sealed cells before generation

        if cfg.seed is not None:
            random.seed(cfg.seed)

        for _ in self.generator.generate(self.grid):
            pass

        reseal_brand(self.grid)            # restore walls on sealed cells after generation

        if not cfg.perfect:
            add_loops(self.grid)

    def solve(self):
        path = None
        came_from = None
        path_cells = None

        for event, *data in self.solver.solve(self.grid):
            if event == 'exploring':
                os.system('clear')
                self.renderer.render(
                    self.grid,
                    exploring=(data[0].y, data[0].x)
                )
            elif event == 'solution':
                path_cells = data[0]
                came_from = data[1]
                path = {(cell.y, cell.x) for cell in path_cells}
                os.system('clear')
                self.renderer.render(self.grid, path=path)
                break
        return path_cells, came_from

    def run(self):
        self.build()
        path_cells, came_from = self.solve()
        self.grid.print_grid(path=path_cells, came_from=came_from)
