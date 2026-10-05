"""Sound effects, background music, and mute control."""

import os

import pygame

from config import SOUNDS_DIR
from sounds.generate_sounds import generate_all


class SoundManager:
    """Loads and plays game sounds with mute support."""

    def __init__(self):
        self.muted = False
        self.music_paused = False
        self.sounds: dict[str, pygame.mixer.Sound] = {}
        self._load_sounds()

    def _load_sounds(self) -> None:
        if not os.path.exists(os.path.join(SOUNDS_DIR, "flap.wav")):
            generate_all(SOUNDS_DIR)

        for name in ("flap", "score", "hit", "menu"):
            path = os.path.join(SOUNDS_DIR, f"{name}.wav")
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)

        music_path = os.path.join(SOUNDS_DIR, "bg_music.wav")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.35)

    def start_music(self) -> None:
        if not self.muted:
            pygame.mixer.music.play(-1)

    def stop_music(self) -> None:
        pygame.mixer.music.stop()
        self.music_paused = False

    def pause_music(self) -> None:
        if not self.muted:
            pygame.mixer.music.pause()
            self.music_paused = True

    def resume_music(self) -> None:
        if not self.muted and self.music_paused:
            pygame.mixer.music.unpause()
            self.music_paused = False
        elif not self.muted and not pygame.mixer.music.get_busy():
            self.start_music()

    def play(self, name: str) -> None:
        if not self.muted and name in self.sounds:
            self.sounds[name].play()

    def toggle_mute(self) -> bool:
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.pause()
            self.music_paused = True
        else:
            pygame.mixer.music.unpause()
            self.music_paused = False
            if not pygame.mixer.music.get_busy():
                self.start_music()
        return self.muted

    def is_muted(self) -> bool:
        return self.muted
