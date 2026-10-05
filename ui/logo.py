"""Flappy Bird logo for the dashboard menu."""

import os

import pygame

from config import ASSETS_DIR, BIRD_COLOR, BIRD_OUTLINE, SCREEN_WIDTH


class FlappyBirdLogo:
    """Draws and caches the Flappy Bird logo."""

    LOGO_PATH = os.path.join(ASSETS_DIR, "logo_menu.png")
    LOGO_OPACITY = 165

    def __init__(self):
        os.makedirs(ASSETS_DIR, exist_ok=True)
        if os.path.exists(self.LOGO_PATH):
            self.surface = pygame.image.load(self.LOGO_PATH).convert_alpha()
        else:
            self.surface = self._create_logo()
            pygame.image.save(self.surface, self.LOGO_PATH)

    def _create_logo(self) -> pygame.Surface:
        width, height = 420, 210
        logo = pygame.Surface((width, height), pygame.SRCALPHA)

        bird_x, bird_y = 95, 105
        radius = 44
        center = (bird_x, bird_y)
        pygame.draw.circle(logo, BIRD_OUTLINE, center, radius + 4)
        pygame.draw.circle(logo, BIRD_COLOR, center, radius)
        pygame.draw.circle(logo, (255, 255, 255), (bird_x + 16, bird_y - 10), 14)
        pygame.draw.circle(logo, (0, 0, 0), (bird_x + 20, bird_y - 10), 6)
        beak = [(bird_x + 34, bird_y), (bird_x + 62, bird_y - 8), (bird_x + 62, bird_y + 8)]
        pygame.draw.polygon(logo, (255, 100, 0), beak)
        wing = [(bird_x - 12, bird_y + 12), (bird_x - 42, bird_y + 28), (bird_x - 10, bird_y + 34)]
        pygame.draw.polygon(logo, (255, 140, 0), wing)

        title_font = pygame.font.Font(None, 82)

        flappy = title_font.render("FLAPPY", True, (255, 255, 255))
        bird_text = title_font.render("BIRD", True, (255, 220, 50))
        shadow_f = title_font.render("FLAPPY", True, (30, 30, 30))
        shadow_b = title_font.render("BIRD", True, (30, 30, 30))

        logo.blit(shadow_f, (172, 52))
        logo.blit(shadow_b, (172, 112))
        logo.blit(flappy, (170, 50))
        logo.blit(bird_text, (170, 110))

        return logo

    def draw(self, surface: pygame.Surface, y: int = 55) -> None:
        logo = self.surface.copy()
        logo.set_alpha(self.LOGO_OPACITY)
        rect = logo.get_rect(center=(SCREEN_WIDTH // 2, y + logo.get_height() // 2))
        surface.blit(logo, rect)
