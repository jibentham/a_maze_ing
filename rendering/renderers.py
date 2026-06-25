from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from algorithms.base import MazeRenderer

if TYPE_CHECKING:
    from maze.maze_gen import Grid


class ASCIIRenderer(MazeRenderer):
    def __init__(self, colors: Optional[dict[str, str]] = None) -> None:
        self.colors: dict[str, str] = colors or {
            "entrance":  "\033[32m",
            "exit":      "\033[31m",
            "path":      "\033[33m",
            "exploring": "\033[36m",
            "RESET":     "\033[0m",
        }

    def render(
        self,
        grid: Grid,
        exploring: Optional[tuple[int, int]] = None,
        path: Optional[set[tuple[int, int]]] = None
    ) -> None:
        assert grid.entrance is not None
        assert grid.exit is not None
        c = self.colors
        print("+" + "---+".join([""] * (grid.width + 1)))
        for r, row in enumerate(grid.cells):
            mid: str = ""
            bot: str = "+"
            for col, cell in enumerate(row):
                mid += "|" if cell.walls['W'] else " "
                if (r, col) == (grid.entrance.y, grid.entrance.x):
                    mid += f"{c['entrance']} X {c['RESET']}"
                elif (r, col) == (grid.exit.y, grid.exit.x):
                    mid += f"{c['exit']} O {c['RESET']}"
                elif path and (r, col) in path:
                    mid += f"{c['path']} . {c['RESET']}"
                elif exploring and (r, col) == exploring:
                    mid += f"{c['exploring']} ? {c['RESET']}"
                else:
                    mid += "   "
                bot += "---+" if cell.walls['S'] else "   +"
            mid += "|"
            print(mid)
            print(bot)


class UnicodeRenderer(MazeRenderer):
    def __init__(self, colors: Optional[dict[str, str]] = None) -> None:
        defaults: dict[str, str] = {
            "entrance":  "\033[35m",
            "exit":      "\033[31m",
            "path":      "\033[37m",
            "exploring": "\033[37m",
            "wall":      "\033[34m",
            "RESET":     "\033[0m",
        }
        if colors:
            defaults.update(colors)
        self.colors: dict[str, str] = defaults
        self.color_index: int = 0

    def render(
        self,
        grid: Grid,
        exploring: Optional[tuple[int, int]] = None,
        path: Optional[set[tuple[int, int]]] = None
    ) -> None:
        assert grid.entrance is not None
        assert grid.exit is not None
        rows: int = grid.height
        cols: int = grid.width
        total_cols: int = cols + 1 + cols
        total_rows: int = rows + 1 + rows

        canvas: list[list[str]] = [['██'] * total_cols for _ in range(total_rows)]

        for r in range(rows):
            for c in range(cols):
                cell = grid.cells[r][c]
                cy: int = r * 2 + 1
                cx: int = c * 2 + 1
                canvas[cy][cx] = '  '
                if not cell.walls['N']:
                    canvas[cy - 1][cx] = '  '
                if not cell.walls['S']:
                    canvas[cy + 1][cx] = '  '
                if not cell.walls['W']:
                    canvas[cy][cx - 1] = '  '
                if not cell.walls['E']:
                    canvas[cy][cx + 1] = '  '

        markers: dict[tuple[int, int], tuple[str, str]] = {}

        if exploring:
            markers[(exploring[0] * 2 + 1, exploring[1] * 2 + 1)] = ('■■', self.colors['exploring'])
        if path:
            for (pr, pc) in path:
                markers[(pr * 2 + 1, pc * 2 + 1)] = ('■■', self.colors['path'])

        ey: int = grid.entrance.y * 2 + 1
        ex: int = grid.entrance.x * 2 + 1
        xy: int = grid.exit.y * 2 + 1
        xx: int = grid.exit.x * 2 + 1
        markers[(ey, ex)] = ('■■', self.colors['entrance'])
        markers[(xy, xx)] = ('■■', self.colors['exit'])

        for ry, row in enumerate(canvas):
            line: str = ''
            for cx, cell_str in enumerate(row):
                if (ry, cx) in markers:
                    marker, color = markers[(ry, cx)]
                    line += color + marker + self.colors['RESET']
                elif cell_str == '██':
                    line += self.colors['wall'] + '██' + self.colors['RESET']
                else:
                    line += cell_str
            print(line)

        self._print_menu()

    def _print_menu(self) -> None:
        print("\033[37m" + "─" * 40 + "\033[0m")
        print("\033[37mA-Maze-ing\033[0m")
        print("1. Re-generate a new maze")
        print("2. Show/hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        print("Choice? (1-4): ", end='', flush=True)

    def rotate_colors(self) -> None:
        color_schemes: list[dict[str, str]] = [
            {"entrance": "\033[35m", "exit": "\033[31m", "path": "\033[37m", "exploring": "\033[37m", "wall": "\033[34m", "RESET": "\033[0m"},
            {"entrance": "\033[32m", "exit": "\033[33m", "path": "\033[36m", "exploring": "\033[36m", "wall": "\033[35m", "RESET": "\033[0m"},
            {"entrance": "\033[34m", "exit": "\033[35m", "path": "\033[32m", "exploring": "\033[32m", "wall": "\033[31m", "RESET": "\033[0m"},
        ]
        self.color_index = (self.color_index + 1) % len(color_schemes)
        self.colors = color_schemes[self.color_index]
