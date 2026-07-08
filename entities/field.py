"""Campo de futebol com parallax."""

import pygame

from utils.constants import FIELD_BOTTOM, FIELD_TOP, IMAGES_DIR, SCREEN_WIDTH


class Field:
    """Renderiza gramado com linhas e profundidade."""

    def __init__(self):
        self.texture = pygame.image.load(f"{IMAGES_DIR}/field.png").convert()
        self.sign = None
        try:
            self.sign = pygame.image.load(f"{IMAGES_DIR}/sign_goal.png").convert_alpha()
        except pygame.error:
            pass
        self.offset_x = 0.0
        self.tile_width = self.texture.get_width()

    def update(self, scroll_speed: float, dt: float):
        """Atualiza offset do parallax."""
        self.offset_x += scroll_speed * dt
        if self.offset_x >= self.tile_width:
            self.offset_x -= self.tile_width

    def draw(self, surface: pygame.Surface):
        """Desenha campo com profundidade."""
        field_rect = pygame.Rect(0, FIELD_TOP, SCREEN_WIDTH, FIELD_BOTTOM - FIELD_TOP)

        # Bordas do estádio
        pygame.draw.rect(surface, (25, 70, 35), field_rect)
        for i in range(0, SCREEN_WIDTH + self.tile_width, self.tile_width):
            x = i - int(self.offset_x) % self.tile_width - self.tile_width
            surface.blit(self.texture, (x, FIELD_TOP))

        # Linhas laterais
        pygame.draw.line(surface, (240, 240, 240), (0, FIELD_TOP), (SCREEN_WIDTH, FIELD_TOP), 3)
        pygame.draw.line(surface, (240, 240, 240), (0, FIELD_BOTTOM), (SCREEN_WIDTH, FIELD_BOTTOM), 3)

        # Placa de gol
        if self.sign:
            sign_x = SCREEN_WIDTH - 90 + int(self.offset_x * 0.3) % 200 - 200
            surface.blit(self.sign, (sign_x, FIELD_TOP + 30))

        # Sombra de profundidade nas bordas
        shade = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
        for y in range(40):
            alpha = int(y * 3)
            pygame.draw.line(shade, (0, 0, 0, alpha), (0, y), (SCREEN_WIDTH, y))
        surface.blit(shade, (0, FIELD_TOP))
        surface.blit(shade, (0, FIELD_BOTTOM - 40))
