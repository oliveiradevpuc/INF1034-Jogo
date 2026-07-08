"""Gerador de assets visuais e sonoros do jogo."""

import math
import os
import struct
import wave

import pygame

from utils.constants import (
    ASSETS_DIR,
    FONTS_DIR,
    IMAGES_DIR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SOUNDS_DIR,
)


def ensure_dirs():
    """Cria diretórios de assets se não existirem."""
    for path in (IMAGES_DIR, SOUNDS_DIR, FONTS_DIR):
        os.makedirs(path, exist_ok=True)


def save_png(surface: pygame.Surface, path: str):
    """Salva superfície como PNG com transparência."""
    pygame.image.save(surface, path)


def draw_shadow(surface: pygame.Surface, rect: pygame.Rect, alpha: int = 90):
    """Desenha sombra elíptica sob entidade."""
    shadow = pygame.Surface((rect.width + 20, 18), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, alpha), shadow.get_rect())
    surface.blit(shadow, (rect.centerx - shadow.get_width() // 2, rect.bottom - 6))


def generate_field_tile() -> pygame.Surface:
    """Gera tile de gramado com textura."""
    tile = pygame.Surface((128, 128))
    for y in range(128):
        for x in range(128):
            stripe = ((x + y) // 16) % 2
            base = (42, 138, 58) if stripe else (36, 118, 50)
            noise = ((x * 13 + y * 7) % 5) - 2
            color = tuple(max(0, min(255, c + noise)) for c in base)
            tile.set_at((x, y), color)
    # Linhas do campo
    pygame.draw.rect(tile, (240, 240, 240), (0, 0, 128, 128), 2)
    pygame.draw.line(tile, (240, 240, 240), (64, 0), (64, 128), 2)
    return tile


def generate_field_background() -> pygame.Surface:
    """Gera fundo completo do campo."""
    bg = pygame.Surface((SCREEN_WIDTH + 400, FIELD_HEIGHT := 500))
    tile = generate_field_tile()
    for x in range(0, bg.get_width(), 128):
        for y in range(0, bg.get_height(), 128):
            bg.blit(tile, (x, y))
    # Linha central
    cx = bg.get_width() // 2
    pygame.draw.circle(bg, (240, 240, 240), (cx, bg.get_height() // 2), 70, 3)
    pygame.draw.line(bg, (240, 240, 240), (cx, 0), (cx, bg.get_height()), 4)
    # Área do gol (direita)
    pygame.draw.rect(bg, (240, 240, 240), (bg.get_width() - 120, 80, 120, 340), 4)
    return bg


def draw_player_frame(frame: int, state: str) -> pygame.Surface:
    """Desenha um frame do jogador principal."""
    surf = pygame.Surface((64, 80), pygame.SRCALPHA)
    body_color = (30, 90, 200)
    skin = (255, 205, 165)
    shorts = (220, 220, 230)

    # Sombra
    draw_shadow(surf, pygame.Rect(8, 10, 48, 60))

    leg_offset = math.sin(frame * 0.8) * 6 if state in ("run", "dribble") else 0
    if state == "fall":
        # Corpo caído
        pygame.draw.ellipse(surf, body_color, (10, 45, 44, 22))
        pygame.draw.circle(surf, skin, (50, 48), 10)
        pygame.draw.rect(surf, shorts, (18, 52, 20, 12), border_radius=4)
    else:
        # Corpo
        pygame.draw.rect(surf, body_color, (18, 22, 28, 30), border_radius=6)
        pygame.draw.rect(surf, shorts, (16, 48, 32, 16), border_radius=4)
        # Cabeça
        pygame.draw.circle(surf, skin, (32, 16), 11)
        pygame.draw.arc(surf, (20, 20, 20), (24, 10, 16, 10), 0, math.pi, 2)
        # Pernas animadas
        pygame.draw.rect(surf, shorts, (20, 60, 10, 14 + leg_offset))
        pygame.draw.rect(surf, shorts, (34, 60, 10, 14 - leg_offset))
        # Braços
        arm = math.sin(frame * 0.8) * 4
        pygame.draw.rect(surf, skin, (10, 28 + arm, 8, 18), border_radius=3)
        pygame.draw.rect(surf, skin, (46, 28 - arm, 8, 18), border_radius=3)

    return surf


def draw_enemy_frame(frame: int, variant: int, state: str) -> pygame.Surface:
    """Desenha frame de adversário."""
    colors = [
        ((200, 40, 40), (180, 30, 30)),
        ((40, 160, 60), (30, 130, 50)),
        ((200, 140, 30), (170, 110, 20)),
    ]
    body_color, shorts_color = colors[variant % 3]
    surf = pygame.Surface((64, 80), pygame.SRCALPHA)
    skin = (240, 190, 150)
    draw_shadow(surf, pygame.Rect(8, 10, 48, 60))

    if state == "slide":
        pygame.draw.ellipse(surf, body_color, (5, 50, 50, 18))
        pygame.draw.circle(surf, skin, (52, 52), 9)
        pygame.draw.rect(surf, shorts_color, (10, 55, 30, 10), border_radius=3)
    elif state == "recover":
        pygame.draw.rect(surf, body_color, (20, 35, 24, 22), border_radius=5)
        pygame.draw.circle(surf, skin, (32, 28), 10)
    else:
        leg = math.sin(frame * 0.9 + variant) * 7
        pygame.draw.rect(surf, body_color, (18, 22, 28, 28), border_radius=5)
        pygame.draw.rect(surf, shorts_color, (16, 46, 32, 14), border_radius=4)
        pygame.draw.circle(surf, skin, (32, 15), 10)
        pygame.draw.rect(surf, shorts_color, (20, 58, 10, 14 + leg))
        pygame.draw.rect(surf, shorts_color, (34, 58, 10, 14 - leg))

    return surf


def draw_ball_frame(frame: int) -> pygame.Surface:
    """Desenha bola com padrão rotativo."""
    surf = pygame.Surface((28, 28), pygame.SRCALPHA)
    draw_shadow(surf, pygame.Rect(2, 4, 24, 20), 70)
    pygame.draw.circle(surf, (250, 250, 250), (14, 12), 11)
    angle = frame * 0.6
    for i in range(5):
        a = angle + i * (math.pi * 2 / 5)
        px = 14 + math.cos(a) * 7
        py = 12 + math.sin(a) * 7
        pygame.draw.circle(surf, (30, 30, 30), (int(px), int(py)), 3)
    pygame.draw.circle(surf, (200, 200, 200), (14, 12), 11, 2)
    return surf


def generate_spritesheets():
    """Gera todas as spritesheets do jogo."""
    # Jogador: idle, run, dribble, fall
    states = {
        "idle": 4,
        "run": 8,
        "dribble": 8,
        "fall": 6,
    }
    for state, count in states.items():
        frames = [draw_player_frame(i, "dribble" if state == "dribble" else state) for i in range(count)]
        sheet = pygame.Surface((64 * count, 80), pygame.SRCALPHA)
        for i, f in enumerate(frames):
            sheet.blit(f, (i * 64, 0))
        save_png(sheet, f"{IMAGES_DIR}/player_{state}.png")

    # Adversários
    for variant in range(3):
        for state, count in [("run", 8), ("slide", 5), ("recover", 4)]:
            frames = [draw_enemy_frame(i, variant, state) for i in range(count)]
            sheet = pygame.Surface((64 * count, 80), pygame.SRCALPHA)
            for i, f in enumerate(frames):
                sheet.blit(f, (i * 64, 0))
            save_png(sheet, f"{IMAGES_DIR}/enemy_{variant}_{state}.png")

    # Bola
    ball_frames = [draw_ball_frame(i) for i in range(8)]
    ball_sheet = pygame.Surface((28 * 8, 28), pygame.SRCALPHA)
    for i, f in enumerate(ball_frames):
        ball_sheet.blit(f, (i * 28, 0))
    save_png(ball_sheet, f"{IMAGES_DIR}/ball.png")

    # Placas e decoração
    sign = pygame.Surface((80, 100), pygame.SRCALPHA)
    pygame.draw.rect(sign, (180, 140, 60), (10, 20, 60, 70), border_radius=4)
    pygame.draw.rect(sign, (120, 90, 40), (10, 20, 60, 70), 3, border_radius=4)
    font = pygame.font.SysFont("arial", 14, bold=True)
    txt = font.render("GOL", True, (255, 255, 255))
    sign.blit(txt, (22, 48))
    save_png(sign, f"{IMAGES_DIR}/sign_goal.png")

    # Botões UI
    for name, color in [("play", (60, 180, 90)), ("ranking", (60, 130, 220)),
                        ("credits", (200, 160, 50)), ("exit", (200, 70, 70)),
                        ("back", (100, 110, 130))]:
        btn = pygame.Surface((280, 56), pygame.SRCALPHA)
        pygame.draw.rect(btn, color, (0, 0, 280, 56), border_radius=14)
        pygame.draw.rect(btn, (255, 255, 255, 60), (0, 0, 280, 28), border_radius=14)
        pygame.draw.rect(btn, (0, 0, 0, 40), (0, 0, 280, 56), 3, border_radius=14)
        save_png(btn, f"{IMAGES_DIR}/btn_{name}.png")

    # Fundos de menu
    menu_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        t = y / SCREEN_HEIGHT
        color = (
            int(20 + t * 30),
            int(60 + t * 80),
            int(100 + t * 40),
        )
        pygame.draw.line(menu_bg, color, (0, y), (SCREEN_WIDTH, y))
    # Gramado estilizado no fundo
    for i in range(0, SCREEN_WIDTH, 80):
        pygame.draw.rect(menu_bg, (30, 100, 50, 80), (i, SCREEN_HEIGHT - 200, 60, 200))
    save_png(menu_bg, f"{IMAGES_DIR}/menu_bg.png")
    save_png(menu_bg, f"{IMAGES_DIR}/ranking_bg.png")
    save_png(menu_bg, f"{IMAGES_DIR}/gameover_bg.png")

    # Ícones HUD
    for icon, color in [("score", (255, 210, 80)),
                        ("time", (100, 200, 255)),
                        ("speed", (255, 150, 80)),
                        ("record", (200, 100, 255))]:
        ico = pygame.Surface((32, 32), pygame.SRCALPHA)
        pygame.draw.circle(ico, color, (16, 16), 14)
        pygame.draw.circle(ico, (255, 255, 255), (16, 16), 14, 2)
        save_png(ico, f"{IMAGES_DIR}/icon_{icon}.png")

    # Campo parallax
    field = generate_field_background()
    save_png(field, f"{IMAGES_DIR}/field.png")

    # Partícula
    particle = pygame.Surface((8, 8), pygame.SRCALPHA)
    pygame.draw.circle(particle, (255, 255, 200, 200), (4, 4), 4)
    save_png(particle, f"{IMAGES_DIR}/particle.png")

    # Logo
    logo = pygame.Surface((500, 120), pygame.SRCALPHA)
    f = pygame.font.SysFont("arial", 48, bold=True)
    t1 = f.render("FUTEBOL", True, (255, 255, 255))
    t2 = f.render("RUNNER", True, (80, 220, 120))
    logo.blit(t1, (20, 10))
    logo.blit(t2, (200, 55))
    save_png(logo, f"{IMAGES_DIR}/logo.png")


def generate_tone(path: str, freq: float, duration: float, volume: float = 0.4,
                  fade: bool = True, noise: float = 0.0):
    """Gera arquivo WAV com tom simples."""
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        frames = []
        for i in range(n_samples):
            t = i / sample_rate
            env = 1.0
            if fade:
                env = min(1.0, t * 20) * max(0.0, 1.0 - (t / duration) * 0.8)
            val = math.sin(2 * math.pi * freq * t) * volume * env
            if noise:
                val += ((i * 17 % 100) / 100 - 0.5) * noise * env
            val = max(-1.0, min(1.0, val))
            frames.append(struct.pack("<h", int(val * 32767)))
        wf.writeframes(b"".join(frames))


def generate_music(path: str, notes: list, tempo: float = 0.25, volume: float = 0.15):
    """Gera música simples com sequência de notas."""
    sample_rate = 22050
    samples = []
    for freq, dur in notes:
        n = int(sample_rate * dur * tempo)
        for i in range(n):
            t = i / sample_rate
            env = min(1.0, t * 15) * max(0.0, 1.0 - t / (dur * tempo + 0.01))
            val = math.sin(2 * math.pi * freq * t) * volume * env
            # Harmônico
            val += math.sin(2 * math.pi * freq * 2 * t) * volume * 0.2 * env
            val = max(-1.0, min(1.0, val))
            samples.append(struct.pack("<h", int(val * 32767)))
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(samples))


def generate_sounds():
    """Gera todos os efeitos sonoros e músicas."""
    generate_tone(f"{SOUNDS_DIR}/click.wav", 880, 0.08, 0.35)
    generate_tone(f"{SOUNDS_DIR}/kick.wav", 120, 0.15, 0.5, noise=0.3)
    generate_tone(f"{SOUNDS_DIR}/ball.wav", 300, 0.1, 0.25)
    generate_tone(f"{SOUNDS_DIR}/slide.wav", 200, 0.35, 0.45, noise=0.15)
    generate_tone(f"{SOUNDS_DIR}/collision.wav", 80, 0.4, 0.6, noise=0.5)
    generate_tone(f"{SOUNDS_DIR}/gameover.wav", 150, 0.8, 0.4)

    menu_notes = [
        (262, 2), (330, 2), (392, 2), (523, 4),
        (392, 2), (330, 2), (262, 4), (0, 1),
    ] * 4
    generate_music(f"{SOUNDS_DIR}/menu_music.wav", menu_notes, 0.3, 0.12)

    game_notes = [
        (196, 1), (220, 1), (247, 1), (262, 1),
        (247, 1), (220, 1), (196, 2), (0, 0.5),
    ] * 8
    generate_music(f"{SOUNDS_DIR}/game_music.wav", game_notes, 0.2, 0.1)


def assets_exist() -> bool:
    """Verifica se assets principais já foram gerados."""
    required = [
        f"{IMAGES_DIR}/player_run.png",
        f"{IMAGES_DIR}/field.png",
        f"{SOUNDS_DIR}/click.wav",
        f"{IMAGES_DIR}/logo.png",
    ]
    return all(os.path.exists(p) for p in required)


def generate_all():
    """Gera todos os assets do projeto."""
    ensure_dirs()
    pygame.init()
    pygame.font.init()
    generate_spritesheets()
    generate_sounds()
    print("Assets gerados com sucesso!")


if __name__ == "__main__":
    generate_all()
