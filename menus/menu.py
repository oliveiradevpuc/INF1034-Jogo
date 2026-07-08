"""Classe base para menus."""

import math
import random

import pygame

from utils.button import Button
from utils.constants import COLOR_WHITE, IMAGES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class MenuBase:
    """Base para telas de menu."""

    def __init__(self, fonts: dict, sounds: dict):
        self.fonts = fonts
        self.sounds = sounds
        self.buttons: list[Button] = []
        self.bg_offset = 0.0
        self.bg_image = None
        self._load_background()

    def _load_background(self):
        try:
            self.bg_image = pygame.image.load(f"{IMAGES_DIR}/menu_bg.png").convert()
        except pygame.error:
            self.bg_image = None

    def play_click(self):
        if "click" in self.sounds:
            self.sounds["click"].play()

    def update(self, dt: float, mouse_pos: tuple):
        """Atualiza animação de fundo e botões."""
        self.bg_offset += dt * 30
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def draw_background(self, surface: pygame.Surface, animated: bool = True):
        """Desenha fundo com parallax leve."""
        if self.bg_image:
            surface.blit(self.bg_image, (0, 0))
            if animated:
                for i in range(5):
                    x = (i * 280 - int(self.bg_offset) % 280) % (SCREEN_WIDTH + 280) - 140
                    y = SCREEN_HEIGHT - 180 + math.sin(self.bg_offset * 0.02 + i) * 10
                    pygame.draw.ellipse(surface, (40, 120, 60, 80), (x, y, 120, 40))
        else:
            surface.fill((20, 60, 100))

        # Gramado animado no rodapé
        for x in range(0, SCREEN_WIDTH + 60, 60):
            ox = (x - int(self.bg_offset * 0.5) % 60)
            pygame.draw.rect(surface, (35, 110, 55), (ox, SCREEN_HEIGHT - 120, 50, 120))

    def handle_events(self, events: list) -> str | None:
        """Processa eventos. Retorna ação ou None."""
        for event in events:
            for btn in self.buttons:
                if btn.handle_event(event, self.play_click):
                    return btn.text
        return None

    def draw_title(self, surface: pygame.Surface, title: str, subtitle: str = ""):
        title_surf = self.fonts["title"].render(title, True, COLOR_WHITE)
        shadow = self.fonts["title"].render(title, True, (0, 0, 0))
        rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        surface.blit(shadow, (rect.x + 3, rect.y + 3))
        surface.blit(title_surf, rect)
        if subtitle:
            sub = self.fonts["medium"].render(subtitle, True, (180, 220, 200))
            surface.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 155)))

    def _make_button(self, y: int, text: str, callback, image_name: str = None,
                     color=(60, 180, 90)) -> Button:
        img = None
        if image_name:
            try:
                img = pygame.image.load(f"{IMAGES_DIR}/btn_{image_name}.png").convert_alpha()
            except pygame.error:
                pass
        return Button(
            SCREEN_WIDTH // 2 - 140, y, 280, 56, text, self.fonts["button"],
            image=img, color=color, callback=callback,
        )
