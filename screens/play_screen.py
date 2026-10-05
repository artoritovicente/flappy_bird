"""Level selection screen (Easy, Medium, Hard)."""

import pygame

from config import BACK_BTN_COLOR, BACK_BTN_HOVER, Difficulty, SCREEN_WIDTH
from ui.button import Button
from ui.renderer import Renderer


class PlayScreen:
    """Play button screen with three difficulty levels."""

    def __init__(self, title_font: pygame.font.Font, menu_font: pygame.font.Font):
        self.title_font = title_font
        self.menu_font = menu_font

        btn_w, btn_h = 260, 48
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        self.btn_easy = Button(btn_x, 280, btn_w, btn_h, "Easy", menu_font, (60, 160, 90), (80, 190, 110))
        self.btn_medium = Button(btn_x, 345, btn_w, btn_h, "Medium", menu_font, (200, 160, 40), (230, 185, 60))
        self.btn_hard = Button(btn_x, 410, btn_w, btn_h, "Hard", menu_font, (180, 60, 60), (220, 80, 80))
        self.btn_back = Button(btn_x, 490, btn_w, btn_h, "Back", menu_font, BACK_BTN_COLOR, BACK_BTN_HOVER)

    def draw(self, surface: pygame.Surface) -> None:
        Renderer.draw_background(surface)
        panel = pygame.Rect(50, 160, SCREEN_WIDTH - 100, 400)
        Renderer.draw_panel(surface, panel)
        Renderer.draw_text(surface, "Select Level", self.title_font, SCREEN_WIDTH // 2, 210)
        Renderer.draw_text(surface, "Choose your difficulty", self.menu_font, SCREEN_WIDTH // 2, 250)

        mouse_pos = pygame.mouse.get_pos()
        for btn in (self.btn_easy, self.btn_medium, self.btn_hard, self.btn_back):
            btn.update(mouse_pos)
            btn.draw(surface)

    def handle_click(self, pos: tuple[int, int]) -> Difficulty | str | None:
        if self.btn_easy.is_clicked(pos):
            return Difficulty.EASY
        if self.btn_medium.is_clicked(pos):
            return Difficulty.MEDIUM
        if self.btn_hard.is_clicked(pos):
            return Difficulty.HARD
        if self.btn_back.is_clicked(pos):
            return "back"
        return None
