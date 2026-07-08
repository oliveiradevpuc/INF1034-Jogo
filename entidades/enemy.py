"""Adversários com comportamentos variados."""

import math
import random

import pygame

from utils.animation import Animation
from utils.constants import FIELD_BOTTOM, FIELD_TOP, IMAGES_DIR


class EnemyType:
    """Tipos de comportamento."""
    RUNNER = "runner"
    SLIDER = "slider"
    INTERCEPTOR = "interceptor"


class EnemyState:
    """Estados de animação do adversário."""
    RUN = "run"
    SLIDE_PREP = "slide_prep"
    SLIDE = "slide"
    RECOVER = "recover"


class Enemy(pygame.sprite.Sprite):
    """Adversário com IA básica."""

    def __init__(self, x: float, y: float, variant: int, enemy_type: str, scroll_speed: float):
        super().__init__()
        self.x = x
        self.y = y
        self.variant = variant % 3
        self.enemy_type = enemy_type
        self.scroll_speed = scroll_speed
        self.state = EnemyState.RUN
        self.slide_timer = 0.0
        self.slide_prep_time = random.uniform(0.4, 0.9)
        self.slide_duration = 0.55
        self.recover_duration = 0.4
        self.vertical_speed = random.uniform(60, 140) * random.choice([-1, 1])
        self.vertical_phase = random.uniform(0, 6.28)
        self.target_y = y
        self.intercept_strength = random.uniform(1.5, 3.0) if enemy_type == EnemyType.INTERCEPTOR else 0.5

        self.anims = {
            EnemyState.RUN: Animation.from_file(
                f"{IMAGES_DIR}/enemy_{self.variant}_run.png", 64, 80, 8
            ),
            EnemyState.SLIDE: Animation.from_file(
                f"{IMAGES_DIR}/enemy_{self.variant}_slide.png", 64, 80, 5, fps=10
            ),
            EnemyState.RECOVER: Animation.from_file(
                f"{IMAGES_DIR}/enemy_{self.variant}_recover.png", 64, 80, 4, fps=8
            ),
        }
        self.current_anim = self.anims[EnemyState.RUN]
        self.image = self.current_anim.get_frame()
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(0, 0, 38, 48)
        self.slide_hitbox = pygame.Rect(0, 0, 55, 30)
        self.mask = None
        self._update_geometry()

    def _update_geometry(self):
        """Atualiza hitboxes conforme estado."""
        self.image = self.current_anim.get_frame()
        self.rect.topleft = (int(self.x), int(self.y))

        if self.state == EnemyState.SLIDE:
            self.slide_hitbox.center = (self.rect.centerx, self.rect.centery + 15)
            self.hitbox = self.slide_hitbox
        else:
            self.hitbox.center = (self.rect.centerx, self.rect.centery)
            self.slide_hitbox = pygame.Rect(0, 0, 55, 30)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt: float, player_y: float, world_scroll: float):
        """Atualiza movimento e comportamento."""
        # Movimento horizontal (mundo se move, inimigo parece vir da direita)
        self.x -= world_scroll * dt

        # Movimento vertical imprevisível
        self.vertical_phase += dt * random.uniform(1.5, 2.5)
        if self.enemy_type == EnemyType.INTERCEPTOR:
            diff = player_y - self.y
            self.y += diff * self.intercept_strength * dt
        else:
            self.y += self.vertical_speed * dt
            if self.y < FIELD_TOP + 15 or self.y > FIELD_BOTTOM - 75:
                self.vertical_speed *= -1
            self.y += math.sin(self.vertical_phase) * 40 * dt

        self.y = max(FIELD_TOP + 15, min(FIELD_BOTTOM - 75, self.y))

        # Máquina de estados do carrinho
        if self.enemy_type == EnemyType.SLIDER:
            self._update_slide(dt)
        else:
            self.state = EnemyState.RUN
            self.current_anim = self.anims[EnemyState.RUN]

        self.current_anim.update(dt)
        self._update_geometry()

    def _update_slide(self, dt: float):
        """Gerencia preparação, deslize e recuperação do carrinho."""
        if self.state == EnemyState.RUN:
            self.slide_timer += dt
            if self.slide_timer >= self.slide_prep_time:
                self.state = EnemyState.SLIDE
                self.slide_timer = 0.0
                self.anims[EnemyState.SLIDE].reset()
                self.current_anim = self.anims[EnemyState.SLIDE]
        elif self.state == EnemyState.SLIDE:
            self.slide_timer += dt
            self.current_anim = self.anims[EnemyState.SLIDE]
            if self.slide_timer >= self.slide_duration:
                self.state = EnemyState.RECOVER
                self.slide_timer = 0.0
                self.anims[EnemyState.RECOVER].reset()
                self.current_anim = self.anims[EnemyState.RECOVER]
        elif self.state == EnemyState.RECOVER:
            self.slide_timer += dt
            self.current_anim = self.anims[EnemyState.RECOVER]
            if self.slide_timer >= self.recover_duration:
                self.state = EnemyState.RUN
                self.slide_timer = 0.0
                self.current_anim = self.anims[EnemyState.RUN]

    def is_off_screen(self, screen_width: int) -> bool:
        return self.x < -100

    def is_sliding(self) -> bool:
        return self.state == EnemyState.SLIDE

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (int(self.x), int(self.y)))
