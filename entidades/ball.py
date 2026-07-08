"""Bola com animação de rotação."""

import math

import pygame

from utils.animation import Animation
from utils.constants import IMAGES_DIR


class Ball:
    """Bola que acompanha o jogador com offset natural."""

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.offset_x = 18.0
        self.offset_y = 8.0
        self.bob_phase = 0.0
        self.anim = Animation.from_file(f"{IMAGES_DIR}/ball.png", 28, 28, 8, fps=14)
        self.rect = pygame.Rect(0, 0, 22, 22)
        self.glow_phase = 0.0

    def update(self, dt: float, player_x: float, player_y: float, moving: bool):
        """Atualiza posição relativa aos pés do jogador."""
        self.bob_phase += dt * (10 if moving else 4)
        bob = math.sin(self.bob_phase) * (4 if moving else 1.5)
        side = math.sin(self.bob_phase * 0.5) * 3

        self.x = player_x + self.offset_x + side
        self.y = player_y + self.offset_y + bob
        self.rect.center = (int(self.x + 14), int(self.y + 14))
        self.anim.update(dt)
        self.glow_phase += dt * 5

    def draw(self, surface: pygame.Surface, camera_x: float = 0):
        """Desenha bola com leve brilho."""
        frame = self.anim.get_frame()
        draw_x = int(self.x - camera_x)
        draw_y = int(self.y)

        # Efeito visual de brilho
        glow_alpha = int(60 + 40 * math.sin(self.glow_phase))
        glow = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 255, 200, glow_alpha), (18, 18), 14)
        surface.blit(glow, (draw_x - 4, draw_y - 4))

        surface.blit(frame, (draw_x, draw_y))
