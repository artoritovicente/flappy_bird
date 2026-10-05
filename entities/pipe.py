"""Obstacle pipes with configurable difficulty."""

import pygame

from config import GROUND_HEIGHT, PIPE_BORDER, PIPE_COLOR, PIPE_WIDTH, SCREEN_HEIGHT, LevelSettings
from entities.bird import Bird


class Pipe:
    def __init__(self, x: int, gap_y: int, settings: LevelSettings):
        self.x = x
        self.gap_y = gap_y
        self.passed = False
        self.width = PIPE_WIDTH
        self.settings = settings

    def update(self) -> None:
        self.x -= self.settings.pipe_speed

    def off_screen(self) -> bool:
        return self.x + self.width < 0

    def collides_with(self, bird: Bird) -> bool:
        bird_rect = bird.get_rect()
        gap = self.settings.pipe_gap
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_rect = pygame.Rect(
            self.x,
            self.gap_y + gap,
            self.width,
            SCREEN_HEIGHT - GROUND_HEIGHT - (self.gap_y + gap),
        )
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

    def draw(self, surface: pygame.Surface) -> None:
        gap = self.settings.pipe_gap
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_y = self.gap_y + gap
        bottom_h = SCREEN_HEIGHT - GROUND_HEIGHT - bottom_y
        bottom_rect = pygame.Rect(self.x, bottom_y, self.width, bottom_h)
        for rect in (top_rect, bottom_rect):
            pygame.draw.rect(surface, PIPE_COLOR, rect)
            pygame.draw.rect(surface, PIPE_BORDER, rect, 3)
            cap = pygame.Rect(rect.x - 4, rect.y if rect == top_rect else rect.y - 20, rect.width + 8, 20)
            pygame.draw.rect(surface, PIPE_BORDER, cap)
