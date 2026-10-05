"""High score screen showing best scores per level."""

import pygame

from config import BACK_BTN_COLOR, BACK_BTN_HOVER, Difficulty, SCREEN_WIDTH
from managers.high_score_manager import HighScoreManager
from ui.button import Button
from ui.renderer import Renderer


class HighScoreScreen:
    """High score button screen."""

    def __init__(self, title_font: pygame.font.Font, menu_font: pygame.font.Font, small_font: pygame.font.Font):
        self.title_font = title_font
        self.menu_font = menu_font
        self.small_font = small_font

        btn_w, btn_h = 260, 48
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        self.btn_back = Button(btn_x, 540, btn_w, btn_h, "Back", menu_font, BACK_BTN_COLOR, BACK_BTN_HOVER)

    def draw(self, surface: pygame.Surface, high_scores: HighScoreManager) -> None:
        Renderer.draw_background(surface)
        panel = pygame.Rect(50, 160, SCREEN_WIDTH - 100, 400)
        Renderer.draw_panel(surface, panel)
        Renderer.draw_text(surface, "High Scores", self.title_font, SCREEN_WIDTH // 2, 210)

        y = 280
        for difficulty in Difficulty:
            label = difficulty.value.capitalize()
            score = high_scores.get(difficulty)
            Renderer.draw_text(surface, f"{label}: {score}", self.menu_font, SCREEN_WIDTH // 2, y)
            y += 50

        Renderer.draw_text(
            surface,
            f"Best Overall: {high_scores.get_best()}",
            self.small_font,
            SCREEN_WIDTH // 2,
            y + 20,
        )

        mouse_pos = pygame.mouse.get_pos()
        self.btn_back.update(mouse_pos)
        self.btn_back.draw(surface)

    def handle_click(self, pos: tuple[int, int]) -> str | None:
        if self.btn_back.is_clicked(pos):
            return "back"
        return None
