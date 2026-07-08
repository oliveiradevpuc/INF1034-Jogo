"""Gerenciamento de pontuação em tempo real."""

from utils.constants import BASE_SCROLL_SPEED, DIFFICULTY_TIERS, MAX_SCROLL_SPEED, SPEED_RAMP


class ScoreManager:
    """Calcula pontuação, distância e multiplicadores."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reinicia estatísticas da partida."""
        self.distance = 0.0
        self.time_survived = 0.0
        self.score = 0
        self.scroll_speed = BASE_SCROLL_SPEED
        self.difficulty_label = "Normal"
        self.multiplier = 1.0

    def update(self, dt: float):
        """Atualiza métricas a cada frame."""
        self.time_survived += dt
        self.scroll_speed = min(
            MAX_SCROLL_SPEED,
            BASE_SCROLL_SPEED + self.time_survived * SPEED_RAMP,
        )
        self._update_difficulty()
        distance_gain = self.scroll_speed * dt * 0.1
        self.distance += distance_gain
        time_points = dt * 10 * self.multiplier
        dist_points = distance_gain * 2 * self.multiplier
        self.score += int(time_points + dist_points)

    def _update_difficulty(self):
        """Atualiza tier de dificuldade conforme tempo."""
        for low, high, mult, label in DIFFICULTY_TIERS:
            if low <= self.time_survived < high:
                self.multiplier = mult
                self.difficulty_label = label
                break

    @property
    def formatted_time(self) -> str:
        return f"{self.time_survived:.1f}"

    @property
    def formatted_distance(self) -> str:
        return f"{int(self.distance)}m"
