
# A-Maze-ing
 
## Description
 
A-Maze-ing is a terminal-based maze generator and solver written in Python. The program reads a configuration file to set up maze parameters, generates a maze using either a Depth-First Search (DFS) or Prim's algorithm, embeds a visual "42" pattern in the center of the maze, solves it using A\*, and renders it in the terminal with ANSI colors and Unicode block characters.
 
### Project Structure
 
The project is organised into the following packages:
 
```
a_maze_ing/
├── main.py
├── config.txt
├── Makefile
├── maze/               ← Cell and Grid data structures
├── algorithms/         ← Generator, solver, and renderer ABCs and factory
├── rendering/          ← ASCII and Unicode renderers
├── runner/             ← MazeRunner orchestrator
└── config/             ← Configuration file parser
```
 
### Data Structures
 
The maze is represented as a `Grid` object containing a 2D list of `Cell` objects. Each `Cell` stores its coordinates, a dictionary of wall states (`N`, `S`, `E`, `W`), a `visited` flag used during generation, and a `sealed` flag used to protect the "42" brand cells from being carved into during generation.
 
Walls default to `True` (all walls present) and are set to `False` when a passage is carved between two cells. This convention means the generator carves passages by removing walls rather than adding them, which is the standard approach for maze generation algorithms.
 
### Maze Generation
 
Two generation algorithms are implemented:
 
**Depth-First Search (DFS)** — also known as recursive backtracking. Starting from the first cell, the algorithm repeatedly moves to a random unvisited neighbor, carving a passage as it goes, and backtracks when it reaches a dead end. This produces mazes with long winding corridors and relatively few dead ends.
 
**Prim's Algorithm** — starts from a single cell and maintains a list of candidate edges (the frontier) connecting visited cells to unvisited ones. At each step a random edge is chosen from the frontier and the unvisited cell is carved into. This produces mazes with shorter dead ends and a more branchy, organic feel compared to DFS.
 
Both algorithms are implemented as Python generators, yielding each cell as it is visited. This design decision allows the renderer to animate the generation process frame by frame without any changes to the algorithm itself.
 
### The "42" Brand
 
Before generation begins, `brand_maze()` marks a set of cells in the center of the grid whose positions form the digits "4" and "2" using a pixel font pattern. These cells are flagged as `sealed` and skipped by both generation algorithms, so the generator carves around them. After generation completes, `reseal_brand()` restores all walls on sealed cells, ensuring the "42" pattern appears as a solid block of walls in the final maze.
 
### Maze Solving
 
The maze is solved using the **A\* algorithm**, which finds the shortest path from the entrance to the exit. A\* maintains a priority queue of candidate cells ordered by their estimated total cost `f = g + h`, where `g` is the actual cost to reach the cell and `h` is the Manhattan distance heuristic to the exit. This guarantees the shortest path is found while exploring fewer cells than a blind breadth-first search.
 
Like the generators, the solver is implemented as a generator, yielding `('exploring', cell)` events during the search and a final `('solution', path, came_from)` event when the exit is reached. This allows the renderer to animate the solving process.
 
### Rendering
 
Two renderers are implemented:
 
**ASCIIRenderer** — renders the maze using `+`, `-`, and `|` characters. Compact and compatible with any terminal.
 
**UnicodeRenderer** — renders the maze using Unicode block characters (`██` for walls, spaces for passages). Produces a visually richer output that more closely resembles a graphical maze. Each cell maps to a single position in a 2D canvas array, with walls represented by adjacent positions. Color is applied at print time by wrapping each character with ANSI escape codes, keeping the canvas itself free of escape sequences to avoid string slicing issues.
 
Both renderers inherit from the `MazeRenderer` abstract base class, making it straightforward to add new renderers in future.
 
### Design Patterns
 
The project uses several design patterns for modularity:
 
- **Abstract Base Classes** — `MazeGenerator`, `MazeSolver`, and `MazeRenderer` define the interface that all algorithms and renderers must implement.
- **Factory Pattern** — `get_generator()`, `get_solver()`, and `get_renderer()` in `algorithms/__init__.py` allow algorithms to be selected by name from the config file without the runner needing to know about concrete classes.
- **Generator Pattern** — all algorithms yield intermediate states, decoupling the algorithm logic from the rendering and animation logic.
- **Orchestrator Pattern** — `MazeRunner` coordinates the build, solve, and render steps, keeping `main.py` clean and minimal.
### Configuration
 
All parameters are read from `config.txt` using Python's built-in `configparser` module. This includes maze dimensions, entrance and exit coordinates, generation and solving algorithm choices, renderer choice, animation delays, random seed, perfect/imperfect toggle, and ANSI colors for each element.
 
Setting `seed = none` uses Python's default random seeding from the system time, producing a different maze each run. Setting `seed` to any integer guarantees the same maze is generated every time for the same algorithm, which is useful for debugging and reproducibility.
 
Setting `perfect = false` calls `add_loops()` after generation, which randomly removes a percentage of walls to create cycles in the maze, making it imperfect (multiple paths between cells).
 
---
 
## Instructions
 
### Requirements
 
- Python 3.10 or higher
- `make`
- No external Python dependencies at runtime
### Installation
 
Clone the repository and set up the virtual environment:
 
```bash
git clone https://github.com/jibentham/a_maze_ing.git
cd a_maze_ing
make install
```
 
This creates a `.venv` virtual environment and installs `flake8` and `mypy` for linting.
 
### Running
 
```bash
make
```
 
If a tarball (`a_maze_ing-1.0.0.tar.gz`) is present, `make` will unpack it and run the program from the extracted directory. Otherwise it runs directly from the source.
 
To run without unpacking a tarball:
 
```bash
make run
```
 
### Configuration
 
Edit `config.txt` to change maze parameters:
 
```ini
[maze]
width = 12
height = 10
entrance = 0,0
exit = 9,11
seed = none
perfect = true
generation_delay = 0.05
solve_delay = 0.02
 
[algorithms]
generator = prims
solver = astar
renderer = unicode
 
[colors]
entrance = GREEN
exit = RED
path = YELLOW
exploring = CYAN
wall = BLUE
```
 
| Parameter          | Description                                      | Options                                          |
|--------------------|--------------------------------------------------|--------------------------------------------------|
| `width`            | Number of columns in the maze                    | Any positive integer                             |
| `height`           | Number of rows in the maze                       | Any positive integer                             |
| `entrance`         | Entrance coordinates as `row,col`                | Any valid cell coordinate                        |
| `exit`             | Exit coordinates as `row,col`                    | Any valid cell coordinate                        |
| `seed`             | Random seed for reproducibility                  | Any integer, or `none` for random                |
| `perfect`          | Whether to generate a perfect maze               | `true` or `false`                                |
| `generation_delay` | Delay in seconds between generation frames       | Any float, `0` for instant                       |
| `solve_delay`      | Delay in seconds between solver frames           | Any float, `0` for instant                       |
| `generator`        | Maze generation algorithm                        | `dfs`, `prims`                                   |
| `solver`           | Maze solving algorithm                           | `astar`                                          |
| `renderer`         | Rendering style                                  | `ascii`, `unicode`                               |
| `entrance` color   | Color of the entrance marker                     | `RED`, `GREEN`, `YELLOW`, `CYAN`, `BLUE`, `MAGENTA`, `WHITE` |
| `exit` color       | Color of the exit marker                         | Same as above                                    |
| `path` color       | Color of the solution path                       | Same as above                                    |
| `exploring` color  | Color of the current cell being explored         | Same as above                                    |
| `wall` color       | Color of the maze walls (Unicode renderer only)  | Same as above                                    |
 
### Interactive Menu
 
Once the maze is generated and solved, an interactive menu is displayed:
 
```
1. Re-generate a new maze
2. Show/hide path from entry to exit
3. Rotate maze colors
4. Quit
```
 
### Output File
 
After each run, the maze is saved to `output.txt` in the following format:
 
```
f7d5b3a2
e1c4d8f0
...
 
Entrance: 0, 0
Exit: 11, 9
 
NEESSWWNESSE
```
 
- Each row of the maze is encoded as a sequence of hexadecimal values, where each value represents the wall state of a cell as a 4-bit binary number (`N`, `E`, `S`, `W`).
- The entrance and exit coordinates follow.
- The solution path is expressed as a string of cardinal directions (`N`, `S`, `E`, `W`).
### Packaging
 
To create a distributable tarball:
 
```bash
make package
```
 
### Linting
 
To run `flake8` and `mypy --strict`:
 
```bash
make lint
```
 
### Cleaning
 
```bash
make clean      # remove __pycache__ and output.txt
make fclean     # also remove .venv, tarball, and extracted directory
```
 
---
 
## Resources
 
- [Maze generation algorithms — Jamis Buck's blog](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Randomized depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search)
- [Randomized Prim's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim%27s_algorithm)
- [A* search algorithm — Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Python configparser — docs.python.org](https://docs.python.org/3/library/configparser.html)
- [Python abc module — docs.python.org](https://docs.python.org/3/library/abc.html)
- [Python typing module — docs.python.org](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [Unicode block elements — Wikipedia](https://en.wikipedia.org/wiki/Block_Elements)
 
