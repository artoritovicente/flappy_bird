"""Options screen with mute and unmute controls."""

import pygame

from config import BACK_BTN_COLOR, BACK_BTN_HOVER, SCREEN_WIDTH
from managers.sound_manager import SoundManager
from ui.button import Button
from ui.renderer import Renderer


class OptionsScreen:
    """Options button screen for sound settings."""

    def __init__(self, title_font: pygame.font.Font, menu_font: pygame.font.Font, small_font: pygame.font.Font):
        self.title_font = title_font
        self.menu_font = menu_font
        self.small_font = small_font

        btn_w, btn_h = 260, 48
        btn_x = (SCREEN_WIDTH - btn_w) // 2
        self.btn_mute = Button(btn_x, 385, btn_w, btn_h, "Mute Sound", menu_font)
        self.btn_back = Button(btn_x, 490, btn_w, btn_h, "Back", menu_font, BACK_BTN_COLOR, BACK_BTN_HOVER)

    def draw(self, surface: pygame.Surface, sound: SoundManager) -> None:
        Renderer.draw_background(surface)
        panel = pygame.Rect(60, 160, SCREEN_WIDTH - 120, 380)
        Renderer.draw_panel(surface, panel)
        Renderer.draw_text(surface, "Options", self.title_font, SCREEN_WIDTH // 2, 210)

        mute_text = "Sound is MUTED" if sound.is_muted() else "Sound is ON"
        Renderer.draw_text(surface, mute_text, self.small_font, SCREEN_WIDTH // 2, 280)
        Renderer.draw_text(surface, "Background music + effects", self.small_font, SCREEN_WIDTH // 2, 315)

        self.btn_mute.label = "Unmute Sound" if sound.is_muted() else "Mute Sound"
        mouse_pos = pygame.mouse.get_pos()
        for btn in (self.btn_mute, self.btn_back):
            btn.update(mouse_pos)
            btn.draw(surface)

    def handle_click(self, pos: tuple[int, int], sound: SoundManager) -> str | None:
        if self.btn_mute.is_clicked(pos):
            sound.toggle_mute()
            return "toggle_mute"
        if self.btn_back.is_clicked(pos):
            return "back"
        return None
