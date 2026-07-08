"""Detecção de colisão precisa."""

import pygame


class CollisionManager:
    """Gerencia colisões entre jogador e adversários."""

    @staticmethod
    def rect_collision(a: pygame.Rect, b: pygame.Rect, padding: int = 4) -> bool:
        """Colisão por retângulos com margem."""
        shrunk_a = a.inflate(-padding, -padding)
        shrunk_b = b.inflate(-padding, -padding)
        return shrunk_a.colliderect(shrunk_b)

    @staticmethod
    def mask_collision(
        sprite_a: pygame.sprite.Sprite,
        sprite_b: pygame.sprite.Sprite,
        offset: tuple[int, int] = (0, 0),
    ) -> bool:
        """Colisão precisa por máscaras."""
        if not hasattr(sprite_a, "mask") or not hasattr(sprite_b, "mask"):
            return CollisionManager.rect_collision(sprite_a.hitbox, sprite_b.hitbox)
        if sprite_a.mask is None or sprite_b.mask is None:
            return CollisionManager.rect_collision(sprite_a.hitbox, sprite_b.hitbox)
        offset_x = sprite_b.hitbox.x - sprite_a.hitbox.x + offset[0]
        offset_y = sprite_b.hitbox.y - sprite_a.hitbox.y + offset[1]
        return sprite_a.mask.overlap(sprite_b.mask, (offset_x, offset_y)) is not None

    @classmethod
    def check_player_enemies(cls, player, enemies: list) -> tuple[bool, object | None]:
        """Verifica colisão do jogador com qualquer inimigo."""
        for enemy in enemies:
            # Colisão por hitbox (precisa e estável)
            if cls.rect_collision(player.hitbox, enemy.hitbox, padding=6):
                return True, enemy
            # Reforço com máscara para carrinhos
            if enemy.is_sliding() and cls.mask_collision(player, enemy):
                return True, enemy
        return False, None
