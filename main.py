import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from runner import MazeRunner

def main() -> None:
    cfg: Config = Config("config.txt")
    runner: MazeRunner = MazeRunner(cfg)
    runner.run()

if __name__ == "__main__":
    main()
