RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"



class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {'W': True, 'S': True, 'E': True, 'N': True}
        self.default = "1111"
        self.replacement = "0"
        self.binary = ''
        self.hexadecimal = []
        self.visited = False

    def check_walls(self):
        if not self.walls['N']:
            idx = 3
            self.binary = self.default[:idx] + self.replacement + self.default[idx + 1:]
        else:
            self.binary = self.default
        if not self.walls['E']:
            idx = 2
            self.binary = self.binary[:idx] + self.replacement + self.binary[idx + 1:]
        if not self.walls['S']:
            idx = 1
            self.binary = self.binary[:idx] + self.replacement + self.binary[idx + 1:]
        if not self.walls['W']:
            idx = 0
            self.binary = self.binary[:idx] + self.replacement + self.binary[idx + 1:]

    def binary_to_hex(self):
        integer_value = int(self.binary, 2)
        hex_value = hex(integer_value)
        self.hexadecimal.append(hex_value[2:])


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cell_list = []
        self.entrance = None
        self.exit = None

    def populate_grid(self):
        self.cells = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(x, y)
                row.append(cell)
                self.cell_list.append(cell)
            self.cells.append(row)
        self.entrance = self.cells[0][0]
        self.exit = self.cells[self.height - 1][self.width - 1]

    def set_entrance(self, row, col):
        self.entrance = self.cells[row][col]

    def set_exit(self, row, col):
        self.exit = self.cells[row][col]

    def print_grid(self):
        for row in self.cells:
            line = ""
            for cell in row:
                cell.check_walls()
                cell.binary_to_hex()
                line += ''.join(cell.hexadecimal)
            print(line)

    def print_grid_ascii(self, exploring=None, path=None):
    # Top border
        print("+" + "---+".join([""] * (self.width + 1)))

        for r, row in enumerate(self.cells):
            mid = ""
            bot = "+"
            for c, cell in enumerate(row):
                mid += "|" if cell.walls['W'] else " "
                if (r, c) == (self.entrance.y, self.entrance.x):
                    mid += f"{GREEN} X {RESET}"
                elif (r, c) == (self.exit.y, self.exit.x):
                    mid += f"{RED} O {RESET}"
                elif path and (r, c) in path:
                    mid += f"{YELLOW} . {RESET}"
                elif exploring and (r, c) == exploring:
                    mid += f"{CYAN} ? {RESET}"
                else:
                    mid += "   "
                bot += "---+" if cell.walls['S'] else "   +"
            mid += "|"   # rightmost wall
            print(mid)
            print(bot)