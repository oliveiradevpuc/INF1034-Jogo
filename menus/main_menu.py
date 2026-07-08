"""Menu inicial."""

import math

import pygame

from menus.menu import MenuBase
from utils.constants import IMAGES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class MainMenu(MenuBase):
    """Tela principal com botões Jogar, Ranking, Créditos e Sair."""

    def __init__(self, fonts: dict, sounds: dict, callbacks: dict):
        super().__init__(fonts, sounds)
        self.callbacks = callbacks
        self.logo = None
        self.logo_phase = 0.0
        self._load_logo()
        self._create_buttons()

    def _load_logo(self):
        try:
            self.logo = pygame.image.load(f"{IMAGES_DIR}/logo.png").convert_alpha()
        except pygame.error:
            self.logo = None

    def _create_buttons(self):
        start_y = 300
        spacing = 70
        items = [
            ("Jogar", "play", self.callbacks.get("play"), (60, 180, 90)),
            ("Ranking", "ranking", self.callbacks.get("ranking"), (60, 130, 220)),
            ("Créditos", "credits", self.callbacks.get("credits"), (200, 160, 50)),
            ("Sair", "exit", self.callbacks.get("exit"), (200, 70, 70)),
        ]
        for i, (text, img, cb, color) in enumerate(items):
            self.buttons.append(self._make_button(start_y + i * spacing, text, cb, img, color))

    def update(self, dt: float, mouse_pos: tuple):
        super().update(dt, mouse_pos)
        self.logo_phase += dt

    def draw(self, surface: pygame.Surface):
        self.draw_background(surface, animated=True)

        if self.logo:
            scale = 1.0 + math.sin(self.logo_phase * 2) * 0.03
            w = int(self.logo.get_width() * scale)
            h = int(self.logo.get_height() * scale)
            logo_scaled = pygame.transform.smoothscale(self.logo, (w, h))
            rect = logo_scaled.get_rect(center=(SCREEN_WIDTH // 2, 180))
            surface.blit(logo_scaled, rect)
        else:
            self.draw_title(surface, "FUTEBOL RUNNER", "Conduza a bola até o infinito!")

        for btn in self.buttons:
            btn.draw(surface)

        hint = self.fonts["small"].render("W/S ou ↑/↓ para mover durante o jogo", True, (200, 220, 230))
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)))

    def start_music(self):
        if "menu_music" in self.sounds:
            pygame.mixer.music.load(self.sounds["menu_music"])
            pygame.mixer.music.play(-1)
