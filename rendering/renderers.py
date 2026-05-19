from algorithms.base import MazeRender

class ASCIIRenderer(MazeRender):
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


class SilentRenderer(MazeRender):
    """Renders nothing — useful for benchmarking or testing."""
    def render(self, grid, exploring=None, path=None):
        pass