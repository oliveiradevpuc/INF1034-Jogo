"""Botão interativo com hover e animação."""

import pygame

from utils.constants import COLOR_WHITE


class Button:
    """Botão de menu com efeitos visuais e sonoros."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font: pygame.font.Font,
        image: pygame.Surface | None = None,
        color: tuple = (60, 180, 90),
        hover_color: tuple = (90, 220, 120),
        text_color: tuple = COLOR_WHITE,
        callback=None,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.image = image
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.hovered = False
        self.scale = 1.0
        self.target_scale = 1.0
        self.alpha = 255

    def update(self, dt: float, mouse_pos: tuple):
        """Atualiza estado de hover e animação."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.target_scale = 1.06 if self.hovered else 1.0
        self.scale += (self.target_scale - self.scale) * min(1.0, dt * 12)

    def handle_event(self, event: pygame.event.Event, play_click=None) -> bool:
        """Processa clique. Retorna True se acionado."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if play_click:
                    play_click()
                if self.callback:
                    self.callback()
                return True
        return False

    def draw(self, surface: pygame.Surface):
        """Renderiza botão com escala animada."""
        scaled_w = int(self.rect.width * self.scale)
        scaled_h = int(self.rect.height * self.scale)
        draw_rect = pygame.Rect(
            self.rect.centerx - scaled_w // 2,
            self.rect.centery - scaled_h // 2,
            scaled_w,
            scaled_h,
        )
        color = self.hover_color if self.hovered else self.color

        if self.image:
            img = pygame.transform.smoothscale(self.image, (scaled_w, scaled_h))
            if self.hovered:
                bright = pygame.Surface(img.get_size(), pygame.SRCALPHA)
                bright.fill((30, 30, 30, 0))
                img.blit(bright, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            surface.blit(img, draw_rect)
        else:
            pygame.draw.rect(surface, color, draw_rect, border_radius=14)
            pygame.draw.rect(surface, (255, 255, 255, 80), draw_rect, 2, border_radius=14)

        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=draw_rect.center)
        surface.blit(label, label_rect)
