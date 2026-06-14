from algorithms.dfs import DFSGenerator
from algorithms.prims import PrimsGenerator
from algorithms.astar import AStarSolver
from rendering.renderers import ASCIIRenderer, SilentRenderer

GENERATORS = {
    'dfs':   DFSGenerator,
    'prims': PrimsGenerator,
}

SOLVERS = {
    'astar': AStarSolver,
}

RENDERERS = {
    'ascii':  ASCIIRenderer,
}

def get_generator(name):
    cls = GENERATORS.get(name)
    if not cls:
        raise ValueError(f"Unknown generator: '{name}'. Available: {list(GENERATORS.keys())}")
    return cls()

def get_solver(name):
    cls = SOLVERS.get(name)
    if not cls:
        raise ValueError(f"Unknown solver: '{name}'. Available: {list(SOLVERS.keys())}")
    return cls()

def get_renderer(name, colors=None):
    cls = RENDERERS.get(name)
    if not cls:
        raise ValueError(f"Unknown renderer: '{name}'. Available: {list(RENDERERS.keys())}")
    return cls(colors=colors) if colors else cls()
