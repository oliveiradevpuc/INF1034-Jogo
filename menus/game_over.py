"""Tela de Game Over."""

import pygame

from menus.menu import MenuBase
from utils.constants import COLOR_GOLD, COLOR_WHITE, SCREEN_HEIGHT, SCREEN_WIDTH


class GameOverScreen(MenuBase):
    """Tela final com pontuação e salvamento de recorde."""

    def __init__(self, fonts: dict, sounds: dict, ranking_manager, callbacks: dict):
        super().__init__(fonts, sounds)
        self.ranking = ranking_manager
        self.callbacks = callbacks
        self.score = 0
        self.player_name = ""
        self.saved = False
        self.input_active = True
        self.buttons = []
        self._rebuild_buttons()

    def _rebuild_buttons(self):
        self.buttons = [
            self._make_button(SCREEN_HEIGHT - 240, "Salvar Recorde", self._save_record, "play", (60, 180, 90)),
            self._make_button(SCREEN_HEIGHT - 165, "Jogar Novamente", self.callbacks.get("retry"), "ranking", (60, 130, 220)),
            self._make_button(SCREEN_HEIGHT - 90, "Voltar ao Menu", self.callbacks.get("menu"), "back", (100, 110, 130)),
        ]

    def setup(self, score: int):
        """Configura tela com pontuação final."""
        self.score = score
        self.player_name = ""
        self.saved = False
        self.input_active = True
        if "gameover" in self.sounds:
            self.sounds["gameover"].play()

    def _save_record(self):
        if self.saved:
            return
        name = self.player_name.strip() or "Jogador"
        self.ranking.add_entry(name, self.score)
        self.saved = True
        self.play_click()

    def handle_events(self, events: list) -> str | None:
        for event in events:
            if event.type == pygame.KEYDOWN and self.input_active and not self.saved:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    self._save_record()
                elif event.unicode.isprintable() and len(self.player_name) < 20:
                    self.player_name += event.unicode
            result = super().handle_events([event])
            if result:
                return result
        return None

    def draw(self, surface: pygame.Surface):
        try:
            bg = pygame.image.load("assets/images/gameover_bg.png").convert()
            bg.set_alpha(180)
            surface.blit(bg, (0, 0))
        except pygame.error:
            surface.fill((30, 20, 40))

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))

        title = self.fonts["title"].render("GAME OVER", True, (255, 80, 80))
        shadow = self.fonts["title"].render("GAME OVER", True, (0, 0, 0))
        tr = title.get_rect(center=(SCREEN_WIDTH // 2, 120))
        surface.blit(shadow, (tr.x + 3, tr.y + 3))
        surface.blit(title, tr)

        panel = pygame.Surface((500, 200), pygame.SRCALPHA)
        pygame.draw.rect(panel, (10, 25, 45, 220), (0, 0, 500, 200), border_radius=16)
        pygame.draw.rect(panel, (200, 80, 80, 100), (0, 0, 500, 200), 2, border_radius=16)

        score_lbl = self.fonts["medium"].render("Pontuação", True, (180, 200, 220))
        score_val = self.fonts["large"].render(f"{self.score:,}", True, COLOR_GOLD)
        high = self.ranking.get_high_score()
        high_lbl = self.fonts["medium"].render(f"Maior Recorde: {high:,}", True, COLOR_WHITE)
        panel.blit(score_lbl, (40, 30))
        panel.blit(score_val, (40, 55))
        panel.blit(high_lbl, (40, 110))

        if self.ranking.is_high_score(self.score) and not self.saved:
            new_rec = self.fonts["small"].render("★ Novo recorde! Digite seu nome:", True, (255, 220, 100))
            panel.blit(new_rec, (40, 150))

        surface.blit(panel, (SCREEN_WIDTH // 2 - 250, 180))

        # Campo de nome
        input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, 400, 400, 44)
        pygame.draw.rect(surface, (20, 40, 60), input_rect, border_radius=8)
        pygame.draw.rect(surface, (80, 200, 120) if self.input_active else (100, 100, 100),
                         input_rect, 2, border_radius=8)
        name_display = self.player_name + ("|" if self.input_active and not self.saved else "")
        name_surf = self.fonts["medium"].render(name_display or "Seu nome...", True, COLOR_WHITE)
        surface.blit(name_surf, (input_rect.x + 12, input_rect.y + 10))

        if self.saved:
            saved_msg = self.fonts["medium"].render("Recorde salvo!", True, (100, 255, 150))
            surface.blit(saved_msg, saved_msg.get_rect(center=(SCREEN_WIDTH // 2, 460)))

        for btn in self.buttons:
            btn.draw(surface)
