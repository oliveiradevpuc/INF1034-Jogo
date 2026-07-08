"""Tela de ranking."""

import pygame

from menus.menu import MenuBase
from utils.constants import COLOR_GOLD, COLOR_WHITE, SCREEN_HEIGHT, SCREEN_WIDTH


class RankingMenu(MenuBase):
    """Exibe top 10 recordes."""

    def __init__(self, fonts: dict, sounds: dict, ranking_manager, on_back):
        super().__init__(fonts, sounds)
        self.ranking = ranking_manager
        self.buttons = [
            self._make_button(SCREEN_HEIGHT - 100, "Voltar", on_back, "back", (100, 110, 130))
        ]

    def draw(self, surface: pygame.Surface):
        self.draw_background(surface)
        self.draw_title(surface, "RANKING", "Top 10 Melhores Jogadores")

        entries = self.ranking.get_entries()
        panel = pygame.Surface((700, 420), pygame.SRCALPHA)
        pygame.draw.rect(panel, (10, 25, 45, 200), (0, 0, 700, 420), border_radius=16)
        pygame.draw.rect(panel, (80, 200, 120, 80), (0, 0, 700, 420), 2, border_radius=16)
        surface.blit(panel, (SCREEN_WIDTH // 2 - 350, 200))

        # Cabeçalho
        headers = ["#", "Nome", "Pontuação", "Data"]
        positions = [40, 100, 350, 530]
        for h, px in zip(headers, positions):
            txt = self.fonts["medium"].render(h, True, COLOR_GOLD)
            panel.blit(txt, (px, 15))

        surface.blit(panel, (SCREEN_WIDTH // 2 - 350, 200))

        if not entries:
            msg = self.fonts["medium"].render("Nenhum recorde ainda. Seja o primeiro!", True, (180, 200, 220))
            surface.blit(msg, msg.get_rect(center=(SCREEN_WIDTH // 2, 400)))
        else:
            for i, entry in enumerate(entries):
                y = 250 + i * 36
                rank_color = COLOR_GOLD if i < 3 else COLOR_WHITE
                rank = self.fonts["medium"].render(f"{i + 1}", True, rank_color)
                name = self.fonts["medium"].render(entry["name"], True, COLOR_WHITE)
                score = self.fonts["medium"].render(f"{entry['score']:,}", True, (100, 220, 150))
                date = self.fonts["small"].render(entry["date"], True, (160, 180, 200))
                surface.blit(rank, (SCREEN_WIDTH // 2 - 310, y))
                surface.blit(name, (SCREEN_WIDTH // 2 - 250, y))
                surface.blit(score, (SCREEN_WIDTH // 2, y))
                surface.blit(date, (SCREEN_WIDTH // 2 + 180, y + 2))

        for btn in self.buttons:
            btn.draw(surface)
