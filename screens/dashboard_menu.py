"""Main dashboard menu with logo, play, high score, options, and exit."""

import pygame

from config import SCREEN_HEIGHT, SCREEN_WIDTH
from ui.button import Button
from ui.logo import FlappyBirdLogo
from ui.renderer import Renderer


class DashboardMenuScreen:
    """Dashboard menu screen controller."""

    def __init__(self, title_font: pygame.font.Font, menu_font: pygame.font.Font, small_font: pygame.font.Font):
        self.title_font = title_font
        self.menu_font = menu_font
        self.small_font = small_font
        self.logo = FlappyBirdLogo()
        self.show_exit_confirm = False
        self.exit_panel = pygame.Rect(40, 265, SCREEN_WIDTH - 80, 250)

        btn_w, btn_h = 260, 48
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        self.btn_play = Button(btn_x, 300, btn_w, btn_h, "Play", menu_font)
        self.btn_high_score = Button(btn_x, 360, btn_w, btn_h, "High Score", menu_font)
        self.btn_options = Button(btn_x, 420, btn_w, btn_h, "Options", menu_font)
        self.btn_exit = Button(btn_x, 480, btn_w, btn_h, "Exit", menu_font, (180, 60, 60), (220, 80, 80))

        confirm_btn_w = 120
        confirm_btn_h = 44
        gap = 24
        confirm_y = self.exit_panel.bottom - confirm_btn_h - 24
        center_x = self.exit_panel.centerx
        self.btn_exit_yes = Button(
            center_x - confirm_btn_w - gap // 2,
            confirm_y,
            confirm_btn_w,
            confirm_btn_h,
            "Yes",
            small_font,
            (180, 60, 60),
            (220, 80, 80),
        )
        self.btn_exit_no = Button(
            center_x + gap // 2,
            confirm_y,
            confirm_btn_w,
            confirm_btn_h,
            "No",
            small_font,
        )

    def draw(self, surface: pygame.Surface) -> None:
        Renderer.draw_background(surface)
        self.logo.draw(surface, y=55)

        mouse_pos = pygame.mouse.get_pos()
        for btn in (self.btn_play, self.btn_high_score, self.btn_options, self.btn_exit):
            btn.update(mouse_pos)
            btn.draw(surface)

        if self.show_exit_confirm:
            self._draw_exit_confirm(surface, mouse_pos)

    def _draw_exit_confirm(self, surface: pygame.Surface, mouse_pos: tuple[int, int]) -> None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        panel = self.exit_panel
        Renderer.draw_panel(surface, panel)

        title_y = panel.y + 42
        Renderer.draw_text(surface, "Exit Game", self.title_font, panel.centerx, title_y)

        message_rect = pygame.Rect(panel.x + 24, panel.y + 78, panel.width - 48, panel.height - 150)
        Renderer.draw_wrapped_text(
            surface,
            "Do you want to exit the game?",
            self.small_font,
            message_rect,
        )

        for btn in (self.btn_exit_yes, self.btn_exit_no):
            btn.update(mouse_pos)
            btn.draw(surface)

    def handle_click(self, pos: tuple[int, int]) -> str | None:
        if self.show_exit_confirm:
            if self.btn_exit_yes.is_clicked(pos):
                return "exit_yes"
            if self.btn_exit_no.is_clicked(pos):
                self.show_exit_confirm = False
                return "exit_no"
            return None

        if self.btn_play.is_clicked(pos):
            return "play"
        if self.btn_high_score.is_clicked(pos):
            return "high_score"
        if self.btn_options.is_clicked(pos):
            return "options"
        if self.btn_exit.is_clicked(pos):
            self.show_exit_confirm = True
            return "exit_prompt"
        return None
