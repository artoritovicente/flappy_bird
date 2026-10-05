"""Shared drawing helpers for all screens."""

import pygame

from config import GROUND_COLOR, GROUND_HEIGHT, PANEL_COLOR, SCREEN_HEIGHT, SCREEN_WIDTH, SKY_COLOR, TEXT_COLOR, TEXT_SHADOW


class Renderer:
    """Common UI and background rendering utilities."""

    @staticmethod
    def draw_text(
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        x: int,
        y: int,
        center: bool = True,
    ) -> None:
        shadow = font.render(text, True, TEXT_SHADOW)
        main = font.render(text, True, TEXT_COLOR)
        if center:
            shadow_rect = shadow.get_rect(center=(x + 2, y + 2))
            main_rect = main.get_rect(center=(x, y))
        else:
            shadow_rect = shadow.get_rect(topleft=(x + 2, y + 2))
            main_rect = main.get_rect(topleft=(x, y))
        surface.blit(shadow, shadow_rect)
        surface.blit(main, main_rect)

    @staticmethod
    def _wrap_lines(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    @staticmethod
    def draw_wrapped_text(
        surface: pygame.Surface,
        text: str,
        font: pygame.font.Font,
        rect: pygame.Rect,
        line_spacing: int = 6,
    ) -> None:
        """Draw word-wrapped text centered inside a rectangle."""
        lines = Renderer._wrap_lines(text, font, rect.width)
        line_height = font.get_height()
        block_height = len(lines) * line_height + max(0, len(lines) - 1) * line_spacing
        y = rect.y + (rect.height - block_height) // 2

        for line in lines:
            shadow = font.render(line, True, TEXT_SHADOW)
            main = font.render(line, True, TEXT_COLOR)
            shadow_rect = shadow.get_rect(center=(rect.centerx + 2, y + line_height // 2 + 2))
            main_rect = main.get_rect(center=(rect.centerx, y + line_height // 2))
            surface.blit(shadow, shadow_rect)
            surface.blit(main, main_rect)
            y += line_height + line_spacing

    @staticmethod
    def draw_background(surface: pygame.Surface) -> None:
        surface.fill(SKY_COLOR)
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(surface, GROUND_COLOR, ground_rect)
        pygame.draw.line(
            surface,
            (180, 140, 90),
            (0, SCREEN_HEIGHT - GROUND_HEIGHT),
            (SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT),
            3,
        )

    @staticmethod
    def draw_panel(surface: pygame.Surface, rect: pygame.Rect) -> None:
        panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        panel.fill(PANEL_COLOR)
        surface.blit(panel, rect.topleft)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=16)
