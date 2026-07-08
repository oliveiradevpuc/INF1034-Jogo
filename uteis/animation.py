"""Sistema de animação com spritesheets."""

import pygame

from utils.constants import ANIM_FPS


class Animation:
    """Gerencia animação baseada em spritesheet."""

    def __init__(
        self,
        sheet: pygame.Surface,
        frame_width: int,
        frame_height: int,
        frame_count: int,
        fps: float = ANIM_FPS,
        loop: bool = True,
    ):
        self.sheet = sheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.fps = fps
        self.loop = loop
        self.current_frame = 0
        self.elapsed = 0.0
        self.finished = False

    def reset(self):
        """Reinicia animação."""
        self.current_frame = 0
        self.elapsed = 0.0
        self.finished = False

    def update(self, dt: float):
        """Avança frames conforme delta time."""
        if self.finished:
            return
        self.elapsed += dt
        frame_duration = 1.0 / self.fps
        while self.elapsed >= frame_duration:
            self.elapsed -= frame_duration
            self.current_frame += 1
            if self.current_frame >= self.frame_count:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.frame_count - 1
                    self.finished = True
                    break

    def get_frame(self) -> pygame.Surface:
        """Retorna superfície do frame atual."""
        rect = pygame.Rect(
            self.current_frame * self.frame_width,
            0,
            self.frame_width,
            self.frame_height,
        )
        frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), rect)
        return frame

    @classmethod
    def from_file(
        cls,
        path: str,
        frame_width: int,
        frame_height: int,
        frame_count: int,
        fps: float = ANIM_FPS,
        loop: bool = True,
    ) -> "Animation":
        """Cria animação a partir de arquivo PNG."""
        sheet = pygame.image.load(path).convert_alpha()
        return cls(sheet, frame_width, frame_height, frame_count, fps, loop)
