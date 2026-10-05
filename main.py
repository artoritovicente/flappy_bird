"""Flappy Bird - entry point."""

import sys
from pathlib import Path

# Ensure project root is on sys.path (fixes "No module named 'config'")
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from game import Game


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
