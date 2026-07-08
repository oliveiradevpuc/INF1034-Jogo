"""Efeitos de partículas."""

import math
import random

import pygame

from utils.constants import IMAGES_DIR


class Particle:
    """Partícula individual."""

    def __init__(self, x: float, y: float, vx: float, vy: float, life: float, color: tuple):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.size = random.uniform(3, 7)

    def update(self, dt: float) -> bool:
        """Atualiza partícula. Retorna False quando expira."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt
        self.life -= dt
        return self.life > 0

    def draw(self, surface: pygame.Surface):
        """Desenha partícula."""
        alpha = int(255 * (self.life / self.max_life))
        size = max(1, int(self.size * (self.life / self.max_life)))
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        c = (*self.color[:3], alpha)
        pygame.draw.circle(s, c, (size, size), size)
        surface.blit(s, (int(self.x - size), int(self.y - size)))


class ParticleSystem:
    """Gerenciador de partículas."""

    def __init__(self):
        self.particles: list[Particle] = []
        self._texture = None

    def load_texture(self):
        """Carrega textura opcional de partícula."""
        try:
            self._texture = pygame.image.load(f"{IMAGES_DIR}/particle.png").convert_alpha()
        except pygame.error:
            self._texture = None

    def emit_burst(self, x: float, y: float, count: int = 12, color: tuple = (255, 220, 100)):
        """Emite explosão de partículas."""
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(80, 250)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.uniform(0.3, 0.8)
            self.particles.append(Particle(x, y, vx, vy, life, color))

    def update(self, dt: float):
        """Atualiza todas as partículas."""
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface):
        """Desenha partículas."""
        for p in self.particles:
            p.draw(surface)

    def clear(self):
        """Remove todas as partículas."""
        self.particles.clear()
