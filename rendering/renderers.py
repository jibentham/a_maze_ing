from algorithms.base import MazeRenderer


class ASCIIRenderer(MazeRenderer):
    def __init__(self, colors=None):
        self.colors = colors or {
            "entrance":  "\033[32m",
            "exit":      "\033[31m",
            "path":      "\033[33m",
            "exploring": "\033[36m",
            "RESET":     "\033[0m",
        }

    def render(self, grid, exploring=None, path=None):
        c = self.colors
        print("+" + "---+".join([""] * (grid.width + 1)))
        for r, row in enumerate(grid.cells):
            mid = ""
            bot = "+"
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
    def __init__(self, colors=None):
        self.colors = colors or {
            "entrance":  "\033[35m",
            "exit":      "\033[31m",
            "path":      "\033[37m",
            "exploring": "\033[37m",
            "wall":      "\033[34m",
            "RESET":     "\033[0m",
        }
        self.color_index = 0

    def render(self, grid, exploring=None, path=None):
        rows = grid.height
        cols = grid.width

        total_cols = cols + 1 + cols
        total_rows = rows + 1 + rows

        # canvas stores plain text only, no ANSI codes
        canvas = [['██'] * total_cols for _ in range(total_rows)]

        for r in range(rows):
            for c in range(cols):
                cell = grid.cells[r][c]
                cy = r * 2 + 1
                cx = c * 2 + 1

                canvas[cy][cx] = '  '

                if not cell.walls['N']:
                    canvas[cy - 1][cx] = '  '
                if not cell.walls['S']:
                    canvas[cy + 1][cx] = '  '
                if not cell.walls['W']:
                    canvas[cy][cx - 1] = '  '
                if not cell.walls['E']:
                    canvas[cy][cx + 1] = '  '

        # markers stored as (marker, color) tuples in a separate dict
        markers = {}

        if exploring:
            markers[(exploring[0] * 2 + 1, exploring[1] * 2 + 1)] = ('■■', self.colors['exploring'])
        if path:
            for (pr, pc) in path:
                markers[(pr * 2 + 1, pc * 2 + 1)] = ('■■', self.colors['path'])

        # entrance and exit drawn last so they take priority
        ey, ex = grid.entrance.y * 2 + 1, grid.entrance.x * 2 + 1
        xy, xx = grid.exit.y * 2 + 1, grid.exit.x * 2 + 1
        markers[(ey, ex)] = ('■■', self.colors['entrance'])
        markers[(xy, xx)] = ('■■', self.colors['exit'])

        # print row by row, applying color only at print time
        for ry, row in enumerate(canvas):
            line = ''
            for cx, cell in enumerate(row):
                if (ry, cx) in markers:
                    marker, color = markers[(ry, cx)]
                    line += color + marker + self.colors['RESET']
                elif cell == '■■':
                    line += self.colors['wall'] + '■■' + self.colors['RESET']
                else:
                    line += cell
            print(line)

        self._print_menu()

    def _print_menu(self):
        print("\033[37m" + "─" * 40 + "\033[0m")
        print("\033[37mA-Maze-ing\033[0m")
        print("1. Re-generate a new maze")
        print("2. Show/hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        print("Choice? (1-4): ", end='', flush=True)

    def rotate_colors(self):
        color_schemes = [
            {"entrance": "\033[35m", "exit": "\033[31m", "path": "\033[37m", "exploring": "\033[37m", "wall": "\033[34m", "RESET": "\033[0m"},
            {"entrance": "\033[32m", "exit": "\033[33m", "path": "\033[36m", "exploring": "\033[36m", "wall": "\033[35m", "RESET": "\033[0m"},
            {"entrance": "\033[34m", "exit": "\033[35m", "path": "\033[32m", "exploring": "\033[32m", "wall": "\033[31m", "RESET": "\033[0m"},
        ]
        self.color_index = (self.color_index + 1) % len(color_schemes)
        self.colors = color_schemes[self.color_index]
