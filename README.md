# Snake Game (Python, Text-Based)

A simple Snake game for the terminal, implemented in Python (using curses). No graphics required—runs in any terminal or Docker container.

## Features
- Play directly in your terminal
- Arrow keys or WASD to move
- Eat food (*) to grow and score points
- Self-collision ends the game
- Q to quit
- Works in Docker (no graphical dependencies)

## Setup

Create and activate a virtual environment (recommended):

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (Locally)

```zsh
python src/snake/text_snake.py
```

## Run (Docker)

Build the image:
```zsh
docker build -t snake-text .
```
Run the game:
```zsh
docker run --rm -it snake-text
```

## Controls
- Arrow keys or WASD: Move
- Q: Quit

## How to Play
- Steer the snake (@ for head, O for body) to eat food (*) and grow.
- Avoid running into yourself!
- The game wraps at the edges.
- After game over, press any key to exit.

## License
MIT
