"""Jogador principal."""

import pygame

from entities.ball import Ball
from utils.animation import Animation
from utils.constants import (
    FIELD_BOTTOM,
    FIELD_TOP,
    IMAGES_DIR,
    PLAYER_SPEED,
    PLAYER_X,
)


class Player(pygame.sprite.Sprite):
    """Atleta controlado pelo jogador."""

    def __init__(self):
        super().__init__()
        self.x = float(PLAYER_X)
        self.y = float((FIELD_TOP + FIELD_BOTTOM) // 2)
        self.vel_y = 0.0
        self.state = "dribble"  # idle, run, dribble, fall
        self.falling = False
        self.fall_timer = 0.0

        self.animations = {
            "idle": Animation.from_file(f"{IMAGES_DIR}/player_idle.png", 64, 80, 4, fps=6),
            "run": Animation.from_file(f"{IMAGES_DIR}/player_run.png", 64, 80, 8),
            "dribble": Animation.from_file(f"{IMAGES_DIR}/player_dribble.png", 64, 80, 8),
            "fall": Animation.from_file(f"{IMAGES_DIR}/player_fall.png", 64, 80, 6, fps=10, loop=False),
        }
        self.current_anim = self.animations["dribble"]
        self.image = self.current_anim.get_frame()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 36, 50)
        self.mask = None
        self._update_hitbox()
        self.ball = Ball()
        self.moving = False

    def _update_hitbox(self):
        """Atualiza retângulo e máscara de colisão."""
        self.rect.center = (int(self.x + 32), int(self.y + 40))
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom - 8
        self.image = self.current_anim.get_frame()
        self.mask = pygame.mask.from_surface(self.image)

    def handle_input(self, keys, dt: float):
        """Processa movimento vertical."""
        if self.falling:
            return
        self.vel_y = 0.0
        self.moving = False
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vel_y = -PLAYER_SPEED
            self.moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vel_y = PLAYER_SPEED
            self.moving = True

    def update(self, dt: float):
        """Atualiza posição e animação."""
        if self.falling:
            self.fall_timer += dt
            self.current_anim = self.animations["fall"]
            self.current_anim.update(dt)
            self._update_hitbox()
            return

        self.y += self.vel_y * dt
        self.y = max(FIELD_TOP + 20, min(FIELD_BOTTOM - 70, self.y))

        target = "dribble" if self.moving else "idle"
        if self.current_anim is not self.animations[target]:
            self.current_anim = self.animations[target]
            self.current_anim.reset()
        self.current_anim.update(dt)
        self._update_hitbox()
        self.ball.update(dt, self.x, self.y, self.moving or True)

    def trigger_fall(self):
        """Inicia animação de queda."""
        self.falling = True
        self.fall_timer = 0.0
        self.animations["fall"].reset()

    def draw(self, surface: pygame.Surface, camera_x: float = 0):
        """Desenha jogador e bola."""
        draw_x = int(self.x - camera_x)
        surface.blit(self.image, (draw_x, int(self.y)))
        self.ball.draw(surface, camera_x)

    @property
    def fall_complete(self) -> bool:
        return self.falling and self.animations["fall"].finished
