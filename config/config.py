from __future__ import annotations
import configparser
import random
from typing import Optional

ANSI_COLORS: dict[str, str] = {
    "RED":     "\033[31m",
    "GREEN":   "\033[32m",
    "YELLOW":  "\033[33m",
    "CYAN":    "\033[36m",
    "BLUE":    "\033[34m",
    "MAGENTA": "\033[35m",
    "WHITE":   "\033[37m",
    "RESET":   "\033[0m",
}


class Config:
    def __init__(self, path: str = "config.txt") -> None:
        cfg: configparser.ConfigParser = configparser.ConfigParser()
        cfg.read(path)

        # maze
        self.width:    int = cfg.getint("maze", "width")
        self.height:   int = cfg.getint("maze", "height")
        self.entrance: tuple[int, int] = tuple(int(x) for x in cfg.get("maze", "entrance").split(","))  # type: ignore[assignment]
        self.exit:     tuple[int, int] = tuple(int(x) for x in cfg.get("maze", "exit").split(","))  # type: ignore[assignment]
        self.perfect:  bool = cfg.getboolean("maze", "perfect")
        seed:          str = cfg.get("maze", "seed")
        self.seed:     Optional[int] = int(seed) if seed.lower() != "none" else None

        # algorithms
        self.generator: str = cfg.get("algorithms", "generator")
        self.solver:    str = cfg.get("algorithms", "solver")
        self.renderer:  str = cfg.get("algorithms", "renderer", fallback="ascii")

        # delays
        self.generation_delay: float = cfg.getfloat("maze", "generation_delay", fallback=0.05)
        self.solve_delay:      float = cfg.getfloat("maze", "solve_delay", fallback=0.02)

        # colors
        self.colors: dict[str, str] = {
            k: ANSI_COLORS[v.upper()]
            for k, v in cfg.items("colors")
        }
        self.colors["RESET"] = ANSI_COLORS["RESET"]

        # apply seed if set
        if self.seed is not None:
            random.seed(self.seed)
