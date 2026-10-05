"""Game configuration, constants, and enums."""

import os
from dataclasses import dataclass
from enum import Enum, auto

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 720
FPS = 60

SKY_COLOR = (135, 206, 235)
GROUND_COLOR = (222, 184, 135)
PIPE_COLOR = (34, 139, 34)
PIPE_BORDER = (0, 100, 0)
BIRD_COLOR = (255, 215, 0)
BIRD_OUTLINE = (255, 140, 0)
TEXT_COLOR = (255, 255, 255)
TEXT_SHADOW = (40, 40, 40)
BUTTON_COLOR = (46, 139, 87)
BUTTON_HOVER = (60, 179, 113)
BUTTON_TEXT = (255, 255, 255)
PANEL_COLOR = (30, 30, 50, 220)
PAUSE_BTN_COLOR = (70, 130, 180)
PAUSE_BTN_HOVER = (100, 149, 237)
BACK_BTN_COLOR = (65, 105, 225)
BACK_BTN_HOVER = (100, 149, 237)

PIPE_WIDTH = 70
GROUND_HEIGHT = 80

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HIGHSCORE_FILE = os.path.join(BASE_DIR, "highscore.json")


class GameState(Enum):
    MENU = auto()
    LEVEL_SELECT = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    HIGH_SCORE = auto()
    OPTIONS = auto()


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass(frozen=True)
class LevelSettings:
    gravity: float
    flap_strength: float
    pipe_speed: float
    pipe_gap: int
    pipe_spawn_interval: int
    label: str


LEVEL_SETTINGS: dict[Difficulty, LevelSettings] = {
    Difficulty.EASY: LevelSettings(
        gravity=0.38,
        flap_strength=-7.5,
        pipe_speed=3,
        pipe_gap=210,
        pipe_spawn_interval=110,
        label="Easy",
    ),
    Difficulty.MEDIUM: LevelSettings(
        gravity=0.45,
        flap_strength=-8.5,
        pipe_speed=4,
        pipe_gap=180,
        pipe_spawn_interval=90,
        label="Medium",
    ),
    Difficulty.HARD: LevelSettings(
        gravity=0.52,
        flap_strength=-9.5,
        pipe_speed=5.5,
        pipe_gap=150,
        pipe_spawn_interval=75,
        label="Hard",
    ),
}
