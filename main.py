import os
import random
from maze_gen import Cell, Grid
from dfs_backtracker import get_unvisited_neighbors, remove_wall, generate_recursive_backtracker
from prims import generate_prims
from queue import PriorityQueue
from astar import astar_solve


def main():
    maze = Grid(20,20)
    maze.populate_grid()
    maze.set_entrance(3,6)
    maze.set_exit(17,8)

    for _ in generate_prims(maze):
        pass

    path = None
    for event, data in astar_solve(maze):
        os.system('clear')
        if event == 'exploring':
            maze.print_grid_ascii(exploring=(data.y, data.x))
        elif event == 'solution':
            path = {(cell.y, cell.x) for cell in data}
            maze.print_grid_ascii(path=path)
            break


if __name__ == "__main__":
    main()