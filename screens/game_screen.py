"""Gameplay, pause overlay, and game over screen."""

import random

import pygame

from config import (
    GROUND_HEIGHT,
    LEVEL_SETTINGS,
    PAUSE_BTN_COLOR,
    PAUSE_BTN_HOVER,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    Difficulty,
    LevelSettings,
)
from entities.bird import Bird
from entities.pipe import Pipe
from ui.button import Button
from ui.renderer import Renderer


class GameScreen:
    """Handles active gameplay, pause, and game over."""

    def __init__(
        self,
        title_font: pygame.font.Font,
        menu_font: pygame.font.Font,
        score_font: pygame.font.Font,
        small_font: pygame.font.Font,
    ):
        self.title_font = title_font
        self.menu_font = menu_font
        self.score_font = score_font
        self.small_font = small_font

        self.difficulty = Difficulty.MEDIUM
        self.settings: LevelSettings = LEVEL_SETTINGS[self.difficulty]
        self.bird = Bird(100, SCREEN_HEIGHT // 2, self.settings)
        self.pipes: list[Pipe] = []
        self.score = 0
        self.frame_count = 0
        self.is_new_high_score = False
        self.is_paused = False

        self.game_over_panel = pygame.Rect(40, 230, SCREEN_WIDTH - 80, 310)
        btn_w, btn_h = 240, 44
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        restart_y = self.game_over_panel.bottom - btn_h - 68
        menu_y = self.game_over_panel.bottom - btn_h - 16

        self.btn_pause = Button(SCREEN_WIDTH - 90, 15, 75, 36, "Pause", small_font, PAUSE_BTN_COLOR, PAUSE_BTN_HOVER)
        self.btn_resume = Button(btn_x, 340, btn_w, btn_h, "Resume", menu_font)
        self.btn_pause_menu = Button(btn_x, 410, btn_w, btn_h, "Main Menu", menu_font)
        self.btn_restart = Button(btn_x, restart_y, btn_w, btn_h, "Play Again", menu_font)
        self.btn_menu = Button(btn_x, menu_y, btn_w, btn_h, "Main Menu", menu_font)

    def start_level(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
        self.settings = LEVEL_SETTINGS[difficulty]
        self.reset()

    def reset(self) -> None:
        self.score = 0
        self.frame_count = 0
        self.is_new_high_score = False
        self.is_paused = False
        self.bird.set_settings(self.settings)
        self.bird.reset(100, SCREEN_HEIGHT // 2)
        self.pipes.clear()

    def toggle_pause(self) -> bool:
        self.is_paused = not self.is_paused
        self.btn_pause.label = "Resume" if self.is_paused else "Pause"
        return self.is_paused

    def _spawn_pipe(self) -> None:
        min_gap = 120
        max_gap = SCREEN_HEIGHT - GROUND_HEIGHT - self.settings.pipe_gap - 120
        gap_y = random.randint(min_gap, max_gap)
        self.pipes.append(Pipe(SCREEN_WIDTH + 20, gap_y, self.settings))

    def update(self) -> str | None:
        if self.is_paused:
            return None

        self.bird.update()
        self.frame_count += 1

        if self.frame_count % self.settings.pipe_spawn_interval == 0:
            self._spawn_pipe()

        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
                return "score"

            if pipe.collides_with(self.bird):
                return "game_over"

        self.pipes = [p for p in self.pipes if not p.off_screen()]

        if self.bird.y - self.bird.radius <= 0:
            return "game_over"

        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        if self.bird.y + self.bird.radius >= ground_y:
            return "game_over"

        return None

    def draw_playing(self, surface: pygame.Surface) -> None:
        Renderer.draw_background(surface)
        for pipe in self.pipes:
            pipe.draw(surface)
        self.bird.draw(surface)

        level_label = self.settings.label
        Renderer.draw_text(surface, str(self.score), self.score_font, SCREEN_WIDTH // 2, 50)
        Renderer.draw_text(surface, f"Level: {level_label}", self.small_font, SCREEN_WIDTH // 2, 90)

        mouse_pos = pygame.mouse.get_pos()
        self.btn_pause.update(mouse_pos)
        self.btn_pause.draw(surface)

    def draw_paused(self, surface: pygame.Surface) -> None:
        self.draw_playing(surface)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        panel = pygame.Rect(60, 240, SCREEN_WIDTH - 120, 230)
        Renderer.draw_panel(surface, panel)
        Renderer.draw_text(surface, "Paused", self.title_font, SCREEN_WIDTH // 2, 285)

        mouse_pos = pygame.mouse.get_pos()
        for btn in (self.btn_resume, self.btn_pause_menu):
            btn.update(mouse_pos)
            btn.draw(surface)

    def draw_game_over(self, surface: pygame.Surface) -> None:
        self.draw_playing(surface)
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        panel = self.game_over_panel
        Renderer.draw_panel(surface, panel)

        title_y = panel.y + 42
        Renderer.draw_text(surface, "Game Over", self.title_font, panel.centerx, title_y)

        info_rect = pygame.Rect(panel.x + 24, panel.y + 70, panel.width - 48, panel.height - 175)
        score_text = f"Score: {self.score}   Level: {self.settings.label}"
        Renderer.draw_wrapped_text(surface, score_text, self.small_font, info_rect)

        if self.is_new_high_score:
            high_score_rect = pygame.Rect(panel.x + 24, panel.y + 145, panel.width - 48, 40)
            Renderer.draw_wrapped_text(surface, "New High Score!", self.small_font, high_score_rect)

        mouse_pos = pygame.mouse.get_pos()
        for btn in (self.btn_restart, self.btn_menu):
            btn.update(mouse_pos)
            btn.draw(surface)

    def handle_playing_click(self, pos: tuple[int, int]) -> str | None:
        if self.btn_pause.is_clicked(pos):
            return "pause"
        return "flap"

    def handle_paused_click(self, pos: tuple[int, int]) -> str | None:
        if self.btn_resume.is_clicked(pos):
            return "resume"
        if self.btn_pause_menu.is_clicked(pos):
            return "main_menu"
        return None

    def handle_game_over_click(self, pos: tuple[int, int]) -> str | None:
        if self.btn_restart.is_clicked(pos):
            return "restart"
        if self.btn_menu.is_clicked(pos):
            return "main_menu"
        return None
