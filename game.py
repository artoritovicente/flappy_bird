"""Main game controller wiring all screens together."""

import sys
from pathlib import Path

# Ensure project root is on sys.path (fixes "No module named 'config'")
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pygame

from config import FPS, HIGHSCORE_FILE, SCREEN_HEIGHT, SCREEN_WIDTH, Difficulty, GameState
from managers.high_score_manager import HighScoreManager
from managers.sound_manager import SoundManager
from screens.dashboard_menu import DashboardMenuScreen
from screens.game_screen import GameScreen
from screens.high_score_screen import HighScoreScreen
from screens.options_screen import OptionsScreen
from screens.play_screen import PlayScreen


class Game:
    """Main game class managing states, rendering, and input."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 42)
        self.score_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.sound = SoundManager()
        self.high_scores = HighScoreManager(HIGHSCORE_FILE)

        self.dashboard = DashboardMenuScreen(self.title_font, self.menu_font, self.small_font)
        self.play_screen = PlayScreen(self.title_font, self.menu_font)
        self.options_screen = OptionsScreen(self.title_font, self.menu_font, self.small_font)
        self.high_score_screen = HighScoreScreen(self.title_font, self.menu_font, self.small_font)
        self.game_screen = GameScreen(self.title_font, self.menu_font, self.score_font, self.small_font)

        self.state = GameState.MENU
        self.sound.start_music()

    def _end_game(self) -> None:
        self.game_screen.bird.alive = False
        self.sound.play("hit")
        self.game_screen.is_new_high_score = self.high_scores.update(
            self.game_screen.difficulty,
            self.game_screen.score,
        )
        self.state = GameState.GAME_OVER

    def _go_to_menu(self) -> None:
        self.state = GameState.MENU
        self.game_screen.is_paused = False
        self.game_screen.btn_pause.label = "Pause"
        self.sound.resume_music()

    def _start_playing(self, difficulty: Difficulty) -> None:
        self.game_screen.start_level(difficulty)
        self.state = GameState.PLAYING
        self.sound.resume_music()

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if not self._handle_keydown(event.key):
                    return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_click(event.pos)

        return True

    def _handle_keydown(self, key: int) -> bool:
        if key == pygame.K_ESCAPE:
            return self._handle_escape()

        if key == pygame.K_p and self.state in (GameState.PLAYING, GameState.PAUSED):
            self._toggle_pause()
            return True

        if key in (pygame.K_SPACE, pygame.K_UP):
            if self.state == GameState.PLAYING:
                self.game_screen.bird.flap()
                self.sound.play("flap")
            elif self.state == GameState.PAUSED:
                self._resume_from_pause()

        return True

    def _handle_escape(self) -> bool:
        if self.state == GameState.PLAYING:
            self._toggle_pause()
        elif self.state == GameState.PAUSED:
            self._go_to_menu()
        elif self.state in (GameState.LEVEL_SELECT, GameState.HIGH_SCORE, GameState.OPTIONS, GameState.GAME_OVER):
            self._go_to_menu()
        elif self.state == GameState.MENU:
            if self.dashboard.show_exit_confirm:
                self.dashboard.show_exit_confirm = False
                return True
            return False
        return True

    def _toggle_pause(self) -> None:
        if self.state == GameState.PLAYING:
            self.game_screen.toggle_pause()
            self.state = GameState.PAUSED
            self.sound.pause_music()
            self.sound.play("menu")
        elif self.state == GameState.PAUSED:
            self._resume_from_pause()

    def _resume_from_pause(self) -> None:
        self.game_screen.toggle_pause()
        self.state = GameState.PLAYING
        self.sound.resume_music()
        self.sound.play("menu")

    def _handle_mouse_click(self, pos: tuple[int, int]) -> None:
        if self.state == GameState.MENU:
            action = self.dashboard.handle_click(pos)
            if action == "play":
                self.sound.play("menu")
                self.state = GameState.LEVEL_SELECT
            elif action == "high_score":
                self.sound.play("menu")
                self.state = GameState.HIGH_SCORE
            elif action == "options":
                self.sound.play("menu")
                self.state = GameState.OPTIONS
            elif action == "exit_prompt":
                self.sound.play("menu")
            elif action == "exit_yes":
                self.sound.play("menu")
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif action == "exit_no":
                self.sound.play("menu")

        elif self.state == GameState.LEVEL_SELECT:
            result = self.play_screen.handle_click(pos)
            if isinstance(result, Difficulty):
                self.sound.play("menu")
                self._start_playing(result)
            elif result == "back":
                self.sound.play("menu")
                self._go_to_menu()

        elif self.state == GameState.HIGH_SCORE:
            if self.high_score_screen.handle_click(pos) == "back":
                self.sound.play("menu")
                self._go_to_menu()

        elif self.state == GameState.OPTIONS:
            result = self.options_screen.handle_click(pos, self.sound)
            if result == "back":
                self.sound.play("menu")
                self._go_to_menu()
            elif result == "toggle_mute":
                self.sound.play("menu")

        elif self.state == GameState.PLAYING:
            action = self.game_screen.handle_playing_click(pos)
            if action == "pause":
                self._toggle_pause()
            elif action == "flap":
                self.game_screen.bird.flap()
                self.sound.play("flap")

        elif self.state == GameState.PAUSED:
            action = self.game_screen.handle_paused_click(pos)
            if action == "resume":
                self._resume_from_pause()
            elif action == "main_menu":
                self.sound.play("menu")
                self._go_to_menu()

        elif self.state == GameState.GAME_OVER:
            action = self.game_screen.handle_game_over_click(pos)
            if action == "restart":
                self.sound.play("menu")
                self._start_playing(self.game_screen.difficulty)
            elif action == "main_menu":
                self.sound.play("menu")
                self._go_to_menu()

    def _update(self) -> None:
        if self.state != GameState.PLAYING:
            return

        result = self.game_screen.update()
        if result == "score":
            self.sound.play("score")
        elif result == "game_over":
            self._end_game()

    def _draw(self) -> None:
        if self.state == GameState.MENU:
            self.dashboard.draw(self.screen)
        elif self.state == GameState.LEVEL_SELECT:
            self.play_screen.draw(self.screen)
        elif self.state == GameState.PLAYING:
            self.game_screen.draw_playing(self.screen)
        elif self.state == GameState.PAUSED:
            self.game_screen.draw_paused(self.screen)
        elif self.state == GameState.GAME_OVER:
            self.game_screen.draw_game_over(self.screen)
        elif self.state == GameState.HIGH_SCORE:
            self.high_score_screen.draw(self.screen, self.high_scores)
        elif self.state == GameState.OPTIONS:
            self.options_screen.draw(self.screen, self.sound)

    def run(self) -> None:
        running = True
        while running:
            running = self._handle_events()
            self._update()
            self._draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        self.sound.stop_music()
        pygame.quit()
        sys.exit()
