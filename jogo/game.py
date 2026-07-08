"""Classe principal que orquestra o jogo."""

import os
import sys

import pygame

from game.game_session import GameSession
from game.states import GameStateManager
from menus.credits_menu import CreditsMenu
from menus.game_over import GameOverScreen
from menus.main_menu import MainMenu
from menus.ranking_menu import RankingMenu
from save.ranking_manager import RankingManager
from utils.constants import (
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SOUNDS_DIR,
    STATE_CREDITS,
    STATE_GAME_OVER,
    STATE_MENU,
    STATE_PLAYING,
    STATE_RANKING,
    TITLE,
)
from utils.transitions import FadeTransition, ZoomEffect


class Game:
    """Gerenciador principal do Futebol Runner."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fonts = self._load_fonts()
        self.sounds = self._load_sounds()
        self.ranking = RankingManager()
        self.states = GameStateManager()
        self.fade = FadeTransition(0.45)
        self.zoom = ZoomEffect(0.8)
        self.fade_alpha = 0

        self.session = GameSession(self.fonts, self.sounds, self.ranking)
        self.main_menu = MainMenu(self.fonts, self.sounds, {
            "play": self._start_game,
            "ranking": lambda: self._change_state(STATE_RANKING),
            "credits": lambda: self._change_state(STATE_CREDITS),
            "exit": self._quit,
        })
        self.ranking_menu = RankingMenu(
            self.fonts, self.sounds, self.ranking,
            on_back=lambda: self._change_state(STATE_MENU),
        )
        self.credits_menu = CreditsMenu(
            self.fonts, self.sounds,
            on_back=lambda: self._change_state(STATE_MENU),
        )
        self.game_over = GameOverScreen(self.fonts, self.sounds, self.ranking, {
            "retry": self._start_game,
            "menu": lambda: self._change_state(STATE_MENU),
        })

        self.main_menu.start_music()

    def _load_fonts(self) -> dict:
        """Carrega fontes do sistema."""
        return {
            "title": pygame.font.SysFont("segoeui", 56, bold=True),
            "large": pygame.font.SysFont("segoeui", 36, bold=True),
            "medium": pygame.font.SysFont("segoeui", 24),
            "small": pygame.font.SysFont("segoeui", 18),
            "button": pygame.font.SysFont("segoeui", 22, bold=True),
        }

    def _load_sounds(self) -> dict:
        """Carrega efeitos sonoros."""
        sounds = {}
        mapping = {
            "click": "click.wav",
            "kick": "kick.wav",
            "ball": "ball.wav",
            "slide": "slide.wav",
            "collision": "collision.wav",
            "gameover": "gameover.wav",
            "menu_music": "menu_music.wav",
            "game_music": "game_music.wav",
        }
        for key, filename in mapping.items():
            path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(path):
                try:
                    if key.endswith("_music"):
                        sounds[key] = path
                    else:
                        sounds[key] = pygame.mixer.Sound(path)
                        sounds[key].set_volume(0.6)
                except pygame.error:
                    pass
        return sounds

    def _change_state(self, new_state: str):
        """Muda estado com transição fade."""
        def on_fade_complete():
            self.states.change(new_state)
            if new_state == STATE_MENU:
                self.main_menu.start_music()
            self.fade.start_in()

        self.fade.start_out(on_fade_complete)

    def _start_game(self):
        """Inicia nova partida."""
        def on_fade_complete():
            self.states.change(STATE_PLAYING)
            self.session.start()
            self.zoom.start()
            self.fade.start_in()

        self.fade.start_out(on_fade_complete)

    def _quit(self):
        self.running = False

    def _go_game_over(self):
        """Transição para game over."""
        self.game_over.setup(self.session.final_score)
        self._change_state(STATE_GAME_OVER)

    def handle_events(self):
        """Processa fila de eventos."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self._quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.states.current == STATE_PLAYING:
                    self._change_state(STATE_MENU)
                elif self.states.current in (STATE_RANKING, STATE_CREDITS):
                    self._change_state(STATE_MENU)

        mouse_pos = pygame.mouse.get_pos()

        if self.states.current == STATE_MENU:
            self.main_menu.handle_events(events)
        elif self.states.current == STATE_RANKING:
            self.ranking_menu.handle_events(events)
        elif self.states.current == STATE_CREDITS:
            self.credits_menu.handle_events(events)
        elif self.states.current == STATE_GAME_OVER:
            self.game_over.handle_events(events)

    def update(self, dt: float):
        """Atualiza estado atual."""
        mouse_pos = pygame.mouse.get_pos()
        self.fade_alpha = self.fade.update(dt)

        if self.states.current == STATE_MENU:
            self.main_menu.update(dt, mouse_pos)
        elif self.states.current == STATE_RANKING:
            self.ranking_menu.update(dt, mouse_pos)
        elif self.states.current == STATE_CREDITS:
            self.credits_menu.update(dt, mouse_pos)
        elif self.states.current == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            self.session.update(dt, keys)
            if self.session.is_ready_for_game_over_screen() and not self.session.transitioned_to_game_over:
                self.session.transitioned_to_game_over = True
                self._go_game_over()
        elif self.states.current == STATE_GAME_OVER:
            self.game_over.update(dt, mouse_pos)

        zoom_scale = self.zoom.update(dt) if self.states.current == STATE_PLAYING else 1.0
        self._zoom_scale = zoom_scale

    def draw(self):
        """Renderiza frame atual."""
        if self.states.current == STATE_MENU:
            self.main_menu.draw(self.screen)
        elif self.states.current == STATE_RANKING:
            self.ranking_menu.draw(self.screen)
        elif self.states.current == STATE_CREDITS:
            self.credits_menu.draw(self.screen)
        elif self.states.current == STATE_PLAYING:
            zoom = getattr(self, "_zoom_scale", 1.0)
            self.session.draw(self.screen, zoom)
        elif self.states.current == STATE_GAME_OVER:
            self.game_over.draw(self.screen)

        self.fade.draw(self.screen, self.fade_alpha)
        pygame.display.flip()

    def run(self):
        """Loop principal."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        sys.exit()
