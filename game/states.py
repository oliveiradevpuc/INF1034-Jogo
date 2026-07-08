"""Estados do jogo."""

from utils.constants import (
    STATE_CREDITS,
    STATE_GAME_OVER,
    STATE_MENU,
    STATE_PLAYING,
    STATE_RANKING,
)


class GameStateManager:
    """Gerencia transições entre estados."""

    def __init__(self):
        self.current = STATE_MENU
        self.previous = STATE_MENU
        self.pending = None

    def change(self, new_state: str):
        """Muda estado imediatamente."""
        self.previous = self.current
        self.current = new_state

    def request_change(self, new_state: str):
        """Agenda mudança (útil com fade)."""
        self.pending = new_state

    def apply_pending(self):
        """Aplica mudança pendente."""
        if self.pending:
            self.change(self.pending)
            self.pending = None

    @property
    def is_playing(self) -> bool:
        return self.current == STATE_PLAYING

    @property
    def is_menu(self) -> bool:
        return self.current == STATE_MENU

    @property
    def is_game_over(self) -> bool:
        return self.current == STATE_GAME_OVER
