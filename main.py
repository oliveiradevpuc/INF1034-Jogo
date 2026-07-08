#!/usr/bin/env python3
"""
Futebol Runner - Jogo de futebol runner 2D em Pygame.

Execute:
    pip install pygame
    python main.py
"""

import os
import sys

# Garante que o diretório do projeto está no path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)


def ensure_assets():
    """Gera assets na primeira execução se necessário."""
    from tools.generate_assets import assets_exist, generate_all
    if not assets_exist():
        print("Gerando assets pela primeira vez...")
        try:
            generate_all()
        except Exception as exc:
            print(f"Aviso: geração Python falhou ({exc}).")
            print("Execute: powershell -File tools/generate_assets.ps1")


def main():
    ensure_assets()
    from game.game import Game
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
