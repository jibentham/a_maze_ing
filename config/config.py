import configparser
import random

ANSI_COLORS = {
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
    def __init__(self, path="config.txt"):
        cfg = configparser.ConfigParser()
        cfg.read(path)

        # maze
        self.width    = cfg.getint("maze", "width")
        self.height   = cfg.getint("maze", "height")
        self.entrance = tuple(int(x) for x in cfg.get("maze", "entrance").split(","))
        self.exit     = tuple(int(x) for x in cfg.get("maze", "exit").split(","))
        self.perfect  = cfg.getboolean("maze", "perfect")
        seed          = cfg.get("maze", "seed")
        self.seed     = int(seed) if seed.lower() != "none" else None

        # algorithms
        self.generator = cfg.get("algorithms", "generator")
        self.solver    = cfg.get("algorithms", "solver")
        self.renderer = cfg.get("algorithms", "renderer", fallback="ascii")

        # colors
        self.colors = {
            k: ANSI_COLORS[v.upper()]
            for k, v in cfg.items("colors")
        }
        self.colors["RESET"] = ANSI_COLORS["RESET"]

        # apply seed if set
        if self.seed is not None:
            random.seed(self.seed)
