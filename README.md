# Futebol Runner

Jogo runner de futebol 2D desenvolvido em Python com Pygame.

## Requisitos

- Python 3.10+
- Pygame 2.5+

## Instalação e execução

```bash
pip install -r requirements.txt
python main.py
```

## Controles

| Tecla | Ação |
|-------|------|
| W / ↑ | Mover para cima |
| S / ↓ | Mover para baixo |
| ESC | Voltar ao menu (durante partida) |
| Mouse | Navegar menus |

## Estrutura do projeto

```
futebol_runner/
├── main.py              # Ponto de entrada
├── assets/              # Imagens, sons e fontes
├── game/                # Lógica principal e sessão
├── entities/            # Jogador, inimigos, bola, campo
├── menus/               # Telas de menu
├── save/                # Pontuação e ranking
├── utils/               # Utilitários compartilhados
└── tools/               # Gerador de assets
```

## Mecânicas

- O jogador avança automaticamente conduzindo a bola
- Desvie de adversários com comportamentos variados (corrida, carrinho, interceptação)
- Pontuação baseada em distância e tempo com multiplicador de dificuldade
- Ranking permanente salvo em `save/ranking.json`

## Autor

Desenvolvido com Python + Pygame
