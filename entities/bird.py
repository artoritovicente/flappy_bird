"""The player-controlled bird."""

import pygame

from config import BIRD_COLOR, BIRD_OUTLINE, LevelSettings


class Bird:
    def __init__(self, x: int, y: int, settings: LevelSettings):
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.radius = 18
        self.alive = True
        self.settings = settings

    def set_settings(self, settings: LevelSettings) -> None:
        self.settings = settings

    def flap(self) -> None:
        self.velocity = self.settings.flap_strength

    def update(self) -> None:
        self.velocity += self.settings.gravity
        self.y += self.velocity

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.x - self.radius,
            int(self.y) - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def draw(self, surface: pygame.Surface) -> None:
        center = (self.x, int(self.y))
        pygame.draw.circle(surface, BIRD_OUTLINE, center, self.radius + 2)
        pygame.draw.circle(surface, BIRD_COLOR, center, self.radius)
        eye = (self.x + 7, int(self.y) - 4)
        pygame.draw.circle(surface, (255, 255, 255), eye, 6)
        pygame.draw.circle(surface, (0, 0, 0), (self.x + 9, int(self.y) - 4), 3)
        beak = [(self.x + 14, int(self.y)), (self.x + 26, int(self.y) - 3), (self.x + 26, int(self.y) + 3)]
        pygame.draw.polygon(surface, (255, 100, 0), beak)

    def reset(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.alive = True
