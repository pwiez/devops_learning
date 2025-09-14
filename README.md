# Snake Game (Python, Pygame)

A simple grid-based Snake game in Python using Pygame. 

## Features
- Arrow keys or WASD to move
- Eat food to grow and score points
- Self-collision ends the game
- Press P to pause/unpause
- Press R, Enter, or Space to restart after game over
- Press Esc or Q to quit
- Toroidal (wrap-around) playfield

## Setup

Create and activate a virtual environment (recommended):

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```zsh
python -m src.snake.main
```

## Packaging/Distribution
- All code is in `src/snake/main.py`.
- No external assets required.
- To package, zip the `src/` folder and `requirements.txt`.

## Controls
- Arrow keys / WASD: Move
- P: Pause/Unpause
- R / Enter / Space: Restart after game over
- Esc / Q: Quit

## How to Play
- Steer the snake to eat red food squares.
- Each food eaten grows the snake and increases your score.
- Avoid running into yourself!
- The game wraps at the edges.
- After game over, press R, Enter, or Space to restart.

## License
MIT
