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
        self.renderer  = get_renderer(config.renderer, config.colors)
        self.path        = None
        self.path_cells  = None
        self.came_from   = None
        self.show_path   = False
        self.color_index = 0

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
        self.path = None
        self.came_from = None
        self.path_cells = None

        for event, *data in self.solver.solve(self.grid):
            if event == 'exploring':
                os.system('clear')
                self.renderer.render(
                    self.grid,
                    exploring=(data[0].y, data[0].x)
                )
            elif event == 'solution':
                self.path_cells = data[0]
                self.came_from = data[1]
                self.path = {(cell.y, cell.x) for cell in self.path_cells}
                os.system('clear')
                self.renderer.render(self.grid)
                break
        return self.path_cells, self.came_from

    def _handle_menu(self, choice):
        if choice == '1':
            self.show_path = False
            self.build()
            self.solve()
        elif choice == '2':
            self.show_path = not self.show_path
            os.system('clear')
            if self.show_path:
                self.renderer.render(self.grid, path=self.path if self.show_path else None)
            else:
                self.renderer.render(self.grid)
        elif choice == '3':
            if hasattr(self.renderer, 'rotate_colors'):
                self.renderer.rotate_colors()
            os.system('clear')
            self.renderer.render(self.grid, path=self.path if self.show_path else None)
        elif choice == '4':
            return False
        return True

    def run(self):
        self.build()
        self.solve()
        self.grid.print_grid(path=self.path_cells, came_from=self.came_from)
        running = True
        while running:
            choice = input()
            running = self._handle_menu(choice)
