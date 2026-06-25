from __future__ import annotations
import os
import random
import time
from typing import Optional
from maze.maze_gen import Cell, Grid
from maze.maze_gen_utils import add_loops, brand_maze, reseal_brand
from algorithms import get_generator, get_solver, get_renderer
from algorithms.base import MazeGenerator, MazeSolver, MazeRenderer
from config import Config


class MazeRunner:
    def __init__(self, config: Config) -> None:
        self.config:      Config = config
        self.grid:        Optional[Grid] = None
        self.generator:   MazeGenerator = get_generator(config.generator)
        self.solver:      MazeSolver = get_solver(config.solver)
        self.renderer:    MazeRenderer = get_renderer(config.renderer, config.colors)
        self.path:        Optional[set[tuple[int, int]]] = None
        self.path_cells:  Optional[list[Cell]] = None
        self.came_from:   Optional[dict[Cell, Cell]] = None
        self.show_path:   bool = False
        self.color_index: int = 0

    def build(self) -> None:
        cfg: Config = self.config
        self.grid = Grid(cfg.width, cfg.height)
        self.grid.populate_grid()
        self.grid.set_entrance(*cfg.entrance)
        self.grid.set_exit(*cfg.exit)

        brand_maze(self.grid)

        if cfg.seed is not None:
            random.seed(cfg.seed)

        for current in self.generator.generate(self.grid):
            os.system('clear')
            self.renderer.render(self.grid, exploring=(current.y, current.x))
            time.sleep(cfg.generation_delay)

        reseal_brand(self.grid)

        if not cfg.perfect:
            add_loops(self.grid)

    def solve(self) -> tuple[Optional[list[Cell]], Optional[dict[Cell, Cell]]]:
        self.path = None
        self.came_from = None
        self.path_cells = None

        assert self.grid is not None

        for event, *data in self.solver.solve(self.grid):
            if event == 'exploring':
                current: Cell = data[0]  # type: ignore[assignment]
                os.system('clear')
                self.renderer.render(
                    self.grid,
                    exploring=(current.y, current.x)
                )
                time.sleep(self.config.solve_delay)
            elif event == 'solution':
                self.path_cells = data[0]  # type: ignore[assignment]
                self.came_from = data[1]   # type: ignore[assignment]
                self.path = {(cell.y, cell.x) for cell in self.path_cells}  # type: ignore[union-attr]
                os.system('clear')
                self.renderer.render(self.grid)
                break

        return self.path_cells, self.came_from

    def _handle_menu(self, choice: str) -> bool:
        assert self.grid is not None
        if choice == '1':
            self.show_path = False
            self.build()
            self.solve()
        elif choice == '2':
            self.show_path = not self.show_path
            os.system('clear')
            self.renderer.render(
                self.grid,
                path=self.path if self.show_path else None
            )
        elif choice == '3':
            if hasattr(self.renderer, 'rotate_colors'):
                self.renderer.rotate_colors()
            os.system('clear')
            self.renderer.render(
                self.grid,
                path=self.path if self.show_path else None
            )
        elif choice == '4':
            return False
        return True

    def run(self) -> None:
        self.build()
        self.solve()

        assert self.grid is not None
        self.grid.print_grid(path=self.path_cells, came_from=self.came_from)

        running: bool = True
        while running:
            choice: str = input()
            running = self._handle_menu(choice)
