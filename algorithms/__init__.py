from __future__ import annotations
from typing import Optional
from algorithms.base import MazeGenerator, MazeSolver, MazeRenderer
from rendering.renderers import ASCIIRenderer, UnicodeRenderer


GENERATORS: dict[str, type[MazeGenerator]] = {}
SOLVERS: dict[str, type[MazeSolver]] = {}
RENDERERS: dict[str, type[ASCIIRenderer] | type[UnicodeRenderer]] = {}


def _register() -> None:
    from algorithms.dfs import DFSGenerator
    from algorithms.prims import PrimsGenerator
    from algorithms.astar import AStarSolver

    GENERATORS['dfs'] = DFSGenerator
    GENERATORS['prims'] = PrimsGenerator
    SOLVERS['astar'] = AStarSolver
    RENDERERS['ascii'] = ASCIIRenderer
    RENDERERS['unicode'] = UnicodeRenderer


_register()


def get_generator(name: str) -> MazeGenerator:
    cls = GENERATORS.get(name)
    if not cls:
        raise ValueError(f"Unknown generator: '{name}'. Available: {list(GENERATORS.keys())}")
    return cls()


def get_solver(name: str) -> MazeSolver:
    cls = SOLVERS.get(name)
    if not cls:
        raise ValueError(f"Unknown solver: '{name}'. Available: {list(SOLVERS.keys())}")
    return cls()


def get_renderer(name: str, colors: Optional[dict[str, str]] = None) -> MazeRenderer:
    cls = RENDERERS.get(name)
    if not cls:
        raise ValueError(f"Unknown renderer: '{name}'. Available: {list(RENDERERS.keys())}")
    return cls(colors=colors)


__all__ = ["get_generator", "get_solver", "get_renderer"]
