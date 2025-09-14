import sys
import pygame

# Window settings
WIDTH, HEIGHT = 640, 480
TITLE = "Snake"
FPS = 1  # render FPS
BG_COLOR = (20, 20, 20)
GRID_SIZE = 20  # pixels per cell
GRID_COLS = WIDTH // GRID_SIZE
GRID_ROWS = HEIGHT // GRID_SIZE
SNAKE_COLOR = (80, 220, 100)
HEAD_COLOR = (120, 255, 140)

# Movement timing (game ticks per second)
TICKS_PER_SECOND = 8
MOVE_EVENT = pygame.USEREVENT + 1
MOVE_INTERVAL_MS = int(1000 / TICKS_PER_SECOND)

# Directions as (dx, dy) on the grid
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def handle_events(direction):
    """Process input events; return (keep_running, new_direction)."""
    new_dir = direction
    keep_running = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                keep_running = False
            # Arrow keys
            elif event.key == pygame.K_UP:
                new_dir = choose_direction(new_dir, UP)
            elif event.key == pygame.K_DOWN:
                new_dir = choose_direction(new_dir, DOWN)
            elif event.key == pygame.K_LEFT:
                new_dir = choose_direction(new_dir, LEFT)
            elif event.key == pygame.K_RIGHT:
                new_dir = choose_direction(new_dir, RIGHT)
            # WASD
            elif event.key == pygame.K_w:
                new_dir = choose_direction(new_dir, UP)
            elif event.key == pygame.K_s:
                new_dir = choose_direction(new_dir, DOWN)
            elif event.key == pygame.K_a:
                new_dir = choose_direction(new_dir, LEFT)
            elif event.key == pygame.K_d:
                new_dir = choose_direction(new_dir, RIGHT)
    return keep_running, new_dir


def choose_direction(current, attempted):
    """Prevent reversing into itself by disallowing exact opposite direction."""
    if (current[0] + attempted[0] == 0) and (current[1] + attempted[1] == 0):
        return current
    return attempted


def wrap_pos(x, y):
    """Wrap position around screen grid (toroidal wrapping)."""
    return x % GRID_COLS, y % GRID_ROWS


def move_snake(snake, direction):
    """Move snake: returns new list of segments with updated head and tail removed."""
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = wrap_pos(head_x + dx, head_y + dy)
    new_snake = [new_head] + snake[:-1]
    return new_snake


def draw_cell(surface, cell, color):
    x, y = cell
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


def render(screen, snake):
    screen.fill(BG_COLOR)
    # Draw body
    for segment in snake[1:]:
        draw_cell(screen, segment, SNAKE_COLOR)
    # Draw head
    draw_cell(screen, snake[0], HEAD_COLOR)
    pygame.display.flip()


def main() -> int:
    pygame.init()
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()

        # Initialize snake centered, length 4, heading right
        start_x, start_y = GRID_COLS // 2, GRID_ROWS // 2
        snake = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y),
            (start_x - 3, start_y),
        ]
        direction = RIGHT

        # Timed movement
        pygame.time.set_timer(MOVE_EVENT, MOVE_INTERVAL_MS)

        running = True
        while running:
            running, direction = handle_events(direction)

            # Tick-based update
            for event in pygame.event.get([MOVE_EVENT]):
                if event.type == MOVE_EVENT:
                    snake = move_snake(snake, direction)

            # Render
            render(screen, snake)

            clock.tick(FPS)
        return 0
    finally:
        pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
