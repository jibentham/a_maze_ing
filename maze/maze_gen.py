from __future__ import annotations
from typing import Optional


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: dict[str, bool] = {'W': True, 'S': True, 'E': True, 'N': True}
        self.default: str = "1111"
        self.replacement: str = "0"
        self.binary: str = ''
        self.hexadecimal: list[str] = []
        self.visited: bool = False
        self.sealed: bool = False

    def check_walls(self) -> None:
        if not self.walls['N']:
            idx: int = 3
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

    def binary_to_hex(self) -> None:
        self.hexadecimal = []
        integer_value: int = int(self.binary, 2)
        hex_value: str = hex(integer_value).upper()
        self.hexadecimal.append(hex_value[2:])


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width: int = width
        self.height: int = height
        self.cell_list: list[Cell] = []
        self.cells: list[list[Cell]] = []
        self.entrance: Optional[Cell] = None
        self.exit: Optional[Cell] = None

    def populate_grid(self) -> None:
        self.cells = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                cell: Cell = Cell(x, y)
                row.append(cell)
                self.cell_list.append(cell)
            self.cells.append(row)
        self.entrance = self.cells[0][0]
        self.exit = self.cells[self.height - 1][self.width - 1]

    def set_entrance(self, row: int, col: int) -> None:
        self.entrance = self.cells[row][col]

    def set_exit(self, row: int, col: int) -> None:
        self.exit = self.cells[row][col]

    def print_grid(
            self,
            filename: str='output.txt',
            path: Optional[list[Cell]]=None,
            came_from: Optional[dict[Cell, Cell]]=None
    ) -> None:
        assert self.entrance is not None
        assert self.exit is not None
        with open(filename, 'w') as f:
            for row in self.cells:
                line: str = ""
                for cell in row:
                    cell.check_walls()
                    cell.binary_to_hex()
                    line += ''.join(cell.hexadecimal)
                f.write(line + '\n')
            f.write(f"\n{self.entrance.x}, {self.entrance.y}\n")
            f.write(f"{self.exit.x}, {self.exit.y}")
            if path and came_from:
                directions = self._extract_directions(path)
                f.write('\n' + directions + '\n')

    def _extract_directions(self, path: list[Cell]) -> str:
        direction_map: dict[tuple[int, int], str] = {
            (-1, 0): 'N',
            (1, 0):  'S',
            (0, 1):  'E',
            (0, -1): 'W',
        }
        result: str = ""
        for i in range(1, len(path)):
            prev: Cell = path[i - 1]
            curr: Cell = path[i]
            dy: int = curr.y - prev.y
            dx: int = curr.x - prev.x
            result += direction_map.get((dy, dx), '?')
        return result
