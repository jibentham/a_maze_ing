from __future__ import annotations
from typing import Optional
import random
from maze.maze_gen import Cell, Grid


DIGITS: dict[str, list[list[int]]] = {
    '4': [
        [1, 0, 0],
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1],
    ],
    '2': [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1],
    ],
}


def is_sealed(cell: Cell) -> bool:
    return cell.sealed


def brand_maze(grid: Grid, char_gap: int = 1) -> None:
    """Mark cells in the center of the maze to display '42'."""
    pattern: list[list[int]] = []
    for digit_row in range(5):
        pattern_row: list[int] = []
        pattern_row += DIGITS['4'][digit_row]
        pattern_row += [0] * char_gap
        pattern_row += DIGITS['2'][digit_row]
        pattern.append(pattern_row)

    pattern_h: int = len(pattern)
    pattern_w: int = len(pattern[0])

    start_r: int = (grid.height - pattern_h) // 2
    start_c: int = (grid.width - pattern_w) // 2

    for pr, pattern_row in enumerate(pattern):
        for pc, cell_val in enumerate(pattern_row):
            if cell_val:
                r: int = start_r + pr
                c: int = start_c + pc
                if 0 <= r < grid.height and 0 <= c < grid.width:
                    grid.cells[r][c].sealed = True


def reseal_brand(grid: Grid) -> None:
    """Restore all walls on sealed cells after generation."""
    for grid_row in grid.cells:
        for cell in grid_row:
            if is_sealed(cell):
                cell.walls = {'N': True, 'S': True, 'E': True, 'W': True}


def add_loops(grid: Grid, count: Optional[int] = None) -> None:
    """Remove extra walls to create loops, making the maze imperfect."""
    count = count or (grid.width * grid.height // 10)
    opposite: dict[str, str] = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    dr: dict[str, tuple[int, int]] = {
        'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)
    }
    removed: int = 0
    while removed < count:
        r: int = random.randint(0, grid.height - 1)
        c: int = random.randint(0, grid.width - 1)
        cell: Cell = grid.cells[r][c]
        if is_sealed(cell):
            continue
        direction: str = random.choice(['N', 'S', 'E', 'W'])
        nr: int = r + dr[direction][0]
        nc: int = c + dr[direction][1]
        if 0 <= nr < grid.height and 0 <= nc < grid.width:
            neighbor: Cell = grid.cells[nr][nc]
            if not is_sealed(neighbor) and cell.walls[direction]:
                cell.walls[direction] = False
                neighbor.walls[opposite[direction]] = False
                removed += 1
