"""Persists high scores per difficulty level."""

import json
import os

from config import Difficulty


class HighScoreManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.scores: dict[str, int] = self._load()

    def _load(self) -> dict[str, int]:
        default = {level.value: 0 for level in Difficulty}
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    for level in Difficulty:
                        default[level.value] = int(data.get(level.value, data.get("high_score", 0)))
            except (json.JSONDecodeError, ValueError, OSError):
                pass
        return default

    def save(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(self.scores, file, indent=2)

    def get(self, difficulty: Difficulty) -> int:
        return self.scores.get(difficulty.value, 0)

    def get_best(self) -> int:
        return max(self.scores.values()) if self.scores else 0

    def update(self, difficulty: Difficulty, score: int) -> bool:
        if score > self.scores.get(difficulty.value, 0):
            self.scores[difficulty.value] = score
            self.save()
            return True
        return False
