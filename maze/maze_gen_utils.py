import random

DIGITS = {
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


def is_sealed(cell):
    return getattr(cell, 'sealed', False)


def brand_maze(grid, char_gap=1):
    """Mark cells in the center of the maze to display '42'."""
    pattern = []
    for row in range(5):
        pattern_row = []
        pattern_row += DIGITS['4'][row]
        pattern_row += [0] * char_gap
        pattern_row += DIGITS['2'][row]
        pattern.append(pattern_row)

    pattern_h = len(pattern)
    pattern_w = len(pattern[0])

    start_r = (grid.height - pattern_h) // 2
    start_c = (grid.width - pattern_w) // 2

    for pr, row in enumerate(pattern):
        for pc, sealed in enumerate(row):
            if sealed:
                r = start_r + pr
                c = start_c + pc
                if 0 <= r < grid.height and 0 <= c < grid.width:
                    grid.cells[r][c].sealed = True


def reseal_brand(grid):
    """Restore all walls on sealed cells after generation."""
    for row in grid.cells:
        for cell in row:
            if is_sealed(cell):
                cell.walls = {'N': True, 'S': True, 'E': True, 'W': True}


def add_loops(grid, count=None):
    """Remove extra walls to create loops, making the maze imperfect."""
    count = count or (grid.width * grid.height // 10)
    opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
    dr = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1)}
    removed = 0
    while removed < count:
        r = random.randint(0, grid.height - 1)
        c = random.randint(0, grid.width - 1)
        cell = grid.cells[r][c]
        if is_sealed(cell):
            continue
        direction = random.choice(['N', 'S', 'E', 'W'])
        nr, nc = r + dr[direction][0], c + dr[direction][1]
        if 0 <= nr < grid.height and 0 <= nc < grid.width:
            if not is_sealed(grid.cells[nr][nc]) and cell.walls[direction]:
                cell.walls[direction] = False
                grid.cells[nr][nc].walls[opposite[direction]] = False
                removed += 1
