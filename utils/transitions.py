"""Transições visuais entre telas."""

import pygame

from utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH


class FadeTransition:
    """Fade in/out entre estados do jogo."""

    def __init__(self, duration: float = 0.5):
        self.duration = duration
        self.elapsed = 0.0
        self.active = False
        self.direction = 1  # 1 = fade out, -1 = fade in
        self.on_complete = None
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill((0, 0, 0))

    def start_out(self, callback=None):
        """Inicia fade para preto."""
        self.active = True
        self.elapsed = 0.0
        self.direction = 1
        self.on_complete = callback

    def start_in(self):
        """Inicia fade de volta."""
        self.active = True
        self.elapsed = 0.0
        self.direction = -1

    def update(self, dt: float) -> int:
        """Retorna alpha do overlay (0-255)."""
        if not self.active:
            return 0
        self.elapsed += dt
        progress = min(1.0, self.elapsed / self.duration)
        if self.direction == 1:
            alpha = int(255 * progress)
            if progress >= 1.0:
                self.active = False
                if self.on_complete:
                    self.on_complete()
        else:
            alpha = int(255 * (1.0 - progress))
            if progress >= 1.0:
                self.active = False
                alpha = 0
        return alpha

    def draw(self, surface: pygame.Surface, alpha: int):
        """Desenha overlay de fade."""
        if alpha > 0:
            self.overlay.set_alpha(alpha)
            surface.blit(self.overlay, (0, 0))


class ZoomEffect:
    """Efeito de zoom leve ao iniciar partida."""

    def __init__(self, duration: float = 0.8):
        self.duration = duration
        self.elapsed = 0.0
        self.active = False

    def start(self):
        """Inicia zoom."""
        self.active = True
        self.elapsed = 0.0

    def update(self, dt: float) -> float:
        """Retorna escala atual (1.0 = normal)."""
        if not self.active:
            return 1.0
        self.elapsed += dt
        t = min(1.0, self.elapsed / self.duration)
        # Zoom de 1.15 para 1.0 com easing
        ease = 1 - (1 - t) ** 3
        scale = 1.15 - 0.15 * ease
        if t >= 1.0:
            self.active = False
            return 1.0
        return scale

    @property
    def is_active(self) -> bool:
        return self.active
