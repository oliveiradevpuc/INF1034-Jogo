"""HUD durante a partida."""

import pygame

from utils.constants import COLOR_GOLD, COLOR_WHITE, IMAGES_DIR, SCREEN_WIDTH


class HUD:
    """Interface heads-up durante o jogo."""

    def __init__(self, fonts: dict):
        self.fonts = fonts
        self.icons = {}
        self._load_icons()

    def _load_icons(self):
        """Carrega ícones do HUD."""
        for name in ("score", "time", "speed", "record"):
            path = f"{IMAGES_DIR}/icon_{name}.png"
            try:
                self.icons[name] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                self.icons[name] = None

    def draw_panel(self, surface: pygame.Surface, x: int, y: int, w: int, h: int):
        """Desenha painel semi-transparente."""
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (10, 25, 45, 180), (0, 0, w, h), border_radius=10)
        pygame.draw.rect(panel, (80, 200, 120, 100), (0, 0, w, h), 2, border_radius=10)
        surface.blit(panel, (x, y))

    def draw_stat(self, surface: pygame.Surface, x: int, y: int, icon_name: str,
                  label: str, value: str):
        """Desenha uma estatística com ícone."""
        if icon_name in self.icons and self.icons[icon_name]:
            surface.blit(self.icons[icon_name], (x, y))
        text_x = x + 38
        lbl = self.fonts["small"].render(label, True, (180, 200, 220))
        val = self.fonts["medium"].render(value, True, COLOR_WHITE)
        surface.blit(lbl, (text_x, y))
        surface.blit(val, (text_x, y + 16))

    def draw(
        self,
        surface: pygame.Surface,
        score: int,
        time_sec: float,
        speed: float,
        high_score: int,
        difficulty: str,
    ):
        """Renderiza HUD completo."""
        self.draw_panel(surface, 20, 15, 280, 110)
        self.draw_stat(surface, 30, 25, "score", "Pontuação", f"{score:,}")
        self.draw_stat(surface, 30, 55, "time", "Tempo", f"{time_sec:.1f}s")

        self.draw_panel(surface, SCREEN_WIDTH - 300, 15, 280, 110)
        self.draw_stat(surface, SCREEN_WIDTH - 290, 25, "speed", "Velocidade", f"{speed:.0f}")
        diff_text = self.fonts["small"].render(f"Dificuldade: {difficulty}", True, COLOR_GOLD)
        surface.blit(diff_text, (SCREEN_WIDTH - 252, 75))
        self.draw_stat(surface, SCREEN_WIDTH - 290, 55, "record", "Recorde", f"{high_score:,}")

        # Barra de progresso de dificuldade
        bar_x, bar_y = SCREEN_WIDTH // 2 - 150, 20
        bar_w, bar_h = 300, 8
        pygame.draw.rect(surface, (30, 50, 70), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        progress = min(1.0, time_sec / 90.0)
        fill_w = int(bar_w * progress)
        if fill_w > 0:
            color = (80, 200, 120) if time_sec < 30 else (255, 200, 80) if time_sec < 60 else (255, 80, 80)
            pygame.draw.rect(surface, color, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
