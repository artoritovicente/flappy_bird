"""Reusable clickable button component."""

import pygame

from config import BUTTON_COLOR, BUTTON_HOVER, BUTTON_TEXT


class Button:
    """Clickable menu button."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        label: str,
        font: pygame.font.Font,
        color: tuple[int, int, int] = BUTTON_COLOR,
        hover_color: tuple[int, int, int] = BUTTON_HOVER,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=12)
        text = self.font.render(self.label, True, BUTTON_TEXT)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)
