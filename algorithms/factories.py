from algorithms.generators.generators import DFSGen, PrimsGen
from algorithms.solvers.solvers import AStarSolve
from rendering.renderers import ASCIIRenderer, SilentRenderer


GENERATORS = {
    'dfs':   DFSGen,
    'prims': PrimsGen,
}

SOLVERS = {
    'astar': AStarSolve,
}

RENDERERS = {
    'ascii':  ASCIIRenderer,
    'silent': SilentRenderer,
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