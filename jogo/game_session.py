"""Sessão de jogo ativa (gameplay)."""

import random

import pygame

from entities.enemy import Enemy, EnemyType
from entities.field import Field
from entities.player import Player
from game.camera import Camera
from game.collision_manager import CollisionManager
from save.score_manager import ScoreManager
from utils.constants import (
    ENEMY_SPAWN_INTERVAL,
    FIELD_BOTTOM,
    FIELD_TOP,
    MAX_ENEMIES,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from utils.hud import HUD
from utils.particles import ParticleSystem


class GameSession:
    """Gerencia partida em andamento."""

    def __init__(self, fonts: dict, sounds: dict, ranking_manager):
        self.fonts = fonts
        self.sounds = sounds
        self.ranking = ranking_manager
        self.score_manager = ScoreManager()
        self.player = Player()
        self.field = Field()
        self.camera = Camera()
        self.hud = HUD(fonts)
        self.particles = ParticleSystem()
        self.enemies: list[Enemy] = []
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = 0.0
        self.game_over = False
        self.game_over_delay = 0.0
        self.collided_enemy = None
        self.particles.load_texture()
        self.transitioned_to_game_over = False

    def reset(self):
        """Reinicia sessão para nova partida."""
        self.score_manager.reset()
        self.player = Player()
        self.field = Field()
        self.camera.reset()
        self.enemies.clear()
        self.enemy_group.empty()
        self.spawn_timer = 0.0
        self.game_over = False
        self.game_over_delay = 0.0
        self.collided_enemy = None
        self.particles.clear()
        self.transitioned_to_game_over = False

    def _play_music(self):
        if "game_music" in self.sounds:
            pygame.mixer.music.load(self.sounds["game_music"])
            pygame.mixer.music.play(-1)

    def start(self):
        """Inicia partida."""
        self.reset()
        self._play_music()

    def _spawn_enemy(self):
        """Cria adversário na borda direita."""
        if len(self.enemies) >= MAX_ENEMIES:
            return
        y = random.uniform(FIELD_TOP + 30, FIELD_BOTTOM - 90)
        x = SCREEN_WIDTH + random.randint(20, 120)
        roll = random.random()
        if roll < 0.25:
            etype = EnemyType.SLIDER
        elif roll < 0.5:
            etype = EnemyType.INTERCEPTOR
        else:
            etype = EnemyType.RUNNER
        variant = random.randint(0, 2)
        enemy = Enemy(x, y, variant, etype, self.score_manager.scroll_speed)
        self.enemies.append(enemy)
        self.enemy_group.add(enemy)

    def update(self, dt: float, keys):
        """Atualiza lógica da partida."""
        if self.game_over:
            self.game_over_delay += dt
            self.player.update(dt)
            self.particles.update(dt)
            return

        self.player.handle_input(keys, dt)
        self.player.update(dt)
        self.score_manager.update(dt)
        self.field.update(self.score_manager.scroll_speed, dt)
        self.camera.update(self.score_manager.scroll_speed, dt)

        self.spawn_timer += dt
        interval = max(0.6, ENEMY_SPAWN_INTERVAL - self.score_manager.time_survived * 0.015)
        if self.spawn_timer >= interval:
            self.spawn_timer = 0.0
            self._spawn_enemy()

        scroll = self.score_manager.scroll_speed
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player.y, scroll)
            if enemy.is_off_screen(SCREEN_WIDTH):
                self.enemies.remove(enemy)
                self.enemy_group.remove(enemy)

        hit, enemy = CollisionManager.check_player_enemies(self.player, self.enemies)
        if hit and not self.player.falling:
            self._trigger_collision(enemy)

        self.particles.update(dt)

    def _trigger_collision(self, enemy):
        """Processa colisão e inicia game over."""
        self.game_over = True
        self.collided_enemy = enemy
        self.player.trigger_fall()
        self.camera.shake(12, 0.4)
        cx = self.player.rect.centerx
        cy = self.player.rect.centery
        self.particles.emit_burst(cx, cy, 20, (255, 180, 60))
        self.particles.emit_burst(cx, cy, 10, (255, 80, 60))
        if enemy and enemy.is_sliding() and "slide" in self.sounds:
            self.sounds["slide"].play()
        if "collision" in self.sounds:
            self.sounds["collision"].play()
        pygame.mixer.music.fadeout(500)

    def draw(self, surface: pygame.Surface, zoom: float = 1.0):
        """Renderiza cena de jogo."""
        shake = self.camera.apply_shake()

        if zoom != 1.0:
            temp = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self._draw_world(temp)
            scaled = pygame.transform.smoothscale(
                temp,
                (int(SCREEN_WIDTH * zoom), int(SCREEN_HEIGHT * zoom)),
            )
            ox = (SCREEN_WIDTH - scaled.get_width()) // 2
            oy = (SCREEN_HEIGHT - scaled.get_height()) // 2
            surface.fill((20, 50, 30))
            surface.blit(scaled, (ox, oy))
        else:
            self._draw_world(surface, shake)

        self.hud.draw(
            surface,
            self.score_manager.score,
            self.score_manager.time_survived,
            self.score_manager.scroll_speed,
            self.ranking.get_high_score(),
            self.score_manager.difficulty_label,
        )
        self.particles.draw(surface)

    def _draw_world(self, surface: pygame.Surface, shake: tuple = (0, 0)):
        """Desenha mundo do jogo."""
        surface.fill((30, 80, 45))
        # Céu/arquibancada
        pygame.draw.rect(surface, (40, 60, 90), (0, 0, SCREEN_WIDTH, 100))
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(surface, (50, 75, 110), (i, 20, 30, 60))

        self.field.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)
        self.player.draw(surface, self.camera.offset_x)

    def is_ready_for_game_over_screen(self) -> bool:
        """Verifica se pode ir para tela de game over."""
        return self.game_over and (
            self.player.fall_complete or self.game_over_delay > 1.5
        )

    @property
    def final_score(self) -> int:
        return self.score_manager.score
