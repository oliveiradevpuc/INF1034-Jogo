"""Constantes globais do jogo."""

# Resolução e performance
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Futebol Runner"

# Caminhos
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"
SAVE_DIR = "save"
RANKING_FILE = f"{SAVE_DIR}/ranking.json"

# Campo de jogo
FIELD_TOP = 120
FIELD_BOTTOM = 620
FIELD_HEIGHT = FIELD_BOTTOM - FIELD_TOP
PLAYER_X = 220

# Velocidade base
BASE_SCROLL_SPEED = 280.0
MAX_SCROLL_SPEED = 680.0
SPEED_RAMP = 8.5

# Multiplicadores de dificuldade (tempo em segundos)
DIFFICULTY_TIERS = [
    (0, 30, 1.0, "Normal"),
    (30, 60, 1.5, "Média"),
    (60, float("inf"), 2.0, "Alta"),
]

# Cores
COLOR_GRASS_DARK = (34, 120, 48)
COLOR_GRASS_LIGHT = (46, 150, 62)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (20, 24, 30)
COLOR_GOLD = (255, 210, 80)
COLOR_RED = (220, 60, 60)
COLOR_BLUE = (50, 120, 220)
COLOR_UI_BG = (15, 35, 55, 200)
COLOR_UI_ACCENT = (80, 200, 120)

# Entidades
PLAYER_SPEED = 420.0
ENEMY_SPAWN_INTERVAL = 1.8
MAX_ENEMIES = 8

# Animação
ANIM_FPS = 12

# Estados do jogo
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_RANKING = "ranking"
STATE_CREDITS = "credits"
STATE_GAME_OVER = "game_over"
