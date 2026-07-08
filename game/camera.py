"""Câmera simples com scroll horizontal."""

from utils.constants import PLAYER_X, SCREEN_WIDTH


class Camera:
    """Câmera que acompanha o scroll do mundo."""

    def __init__(self):
        self.x = 0.0
        self.shake_timer = 0.0
        self.shake_intensity = 0.0

    def update(self, scroll_speed: float, dt: float):
        """Avança câmera com o mundo."""
        self.x += scroll_speed * dt
        if self.shake_timer > 0:
            self.shake_timer -= dt

    def shake(self, intensity: float = 8.0, duration: float = 0.3):
        """Ativa tremor de câmera."""
        self.shake_intensity = intensity
        self.shake_timer = duration

    @property
    def offset_x(self) -> float:
        """Offset visual (jogador fixo, mundo se move)."""
        return 0.0

    def apply_shake(self) -> tuple[int, int]:
        """Retorna deslocamento de shake."""
        if self.shake_timer <= 0:
            return (0, 0)
        import random
        i = self.shake_intensity * (self.shake_timer / 0.3)
        return (int(random.uniform(-i, i)), int(random.uniform(-i, i)))

    def reset(self):
        self.x = 0.0
        self.shake_timer = 0.0
