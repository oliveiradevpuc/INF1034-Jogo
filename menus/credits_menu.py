"""Tela de créditos."""

import pygame

from menus.menu import MenuBase
from utils.constants import COLOR_WHITE, SCREEN_HEIGHT, SCREEN_WIDTH


class CreditsMenu(MenuBase):
    """Exibe informações do projeto."""

    def __init__(self, fonts: dict, sounds: dict, on_back):
        super().__init__(fonts, sounds)
        self.buttons = [
            self._make_button(SCREEN_HEIGHT - 100, "Voltar", on_back, "back", (100, 110, 130))
        ]

    def draw(self, surface: pygame.Surface):
        self.draw_background(surface)
        self.draw_title(surface, "CRÉDITOS")

        lines = [
            ("Projeto", "Futebol Runner"),
            ("Tecnologia", "Python + Pygame"),
            ("Gênero", "Runner de Futebol 2D"),
            ("Autor", "Desenvolvido com Pygame"),
            ("Versão", "1.0.0"),
        ]

        panel = pygame.Surface((600, 340), pygame.SRCALPHA)
        pygame.draw.rect(panel, (10, 25, 45, 200), (0, 0, 600, 340), border_radius=16)
        pygame.draw.rect(panel, (80, 200, 120, 80), (0, 0, 600, 340), 2, border_radius=16)

        for i, (label, value) in enumerate(lines):
            y = 30 + i * 55
            lbl = self.fonts["medium"].render(label + ":", True, (150, 200, 180))
            val = self.fonts["large"].render(value, True, COLOR_WHITE)
            panel.blit(lbl, (40, y))
            panel.blit(val, (40, y + 28))

        surface.blit(panel, (SCREEN_WIDTH // 2 - 300, 220))

        thanks = self.fonts["small"].render("Obrigado por jogar!", True, (180, 220, 200))
        surface.blit(thanks, thanks.get_rect(center=(SCREEN_WIDTH // 2, 580)))

        for btn in self.buttons:
            btn.draw(surface)
