A simple Snake game for the terminal, implemented in Python (using curses). No graphics required—runs in any terminal or Docker container.

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

## License
MIT
