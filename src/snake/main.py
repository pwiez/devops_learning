import sys
import random
import pygame

# Window settings
WIDTH, HEIGHT = 640, 480
TITLE = "Snake"
FPS = 30  # render FPS
BG_COLOR = (20, 20, 20)
GRID_SIZE = 20  # pixels per cell
GRID_COLS = WIDTH // GRID_SIZE
GRID_ROWS = HEIGHT // GRID_SIZE
SNAKE_COLOR = (80, 220, 100)
HEAD_COLOR = (120, 255, 140)
FOOD_COLOR = (240, 80, 80)
HUD_COLOR = (230, 230, 230)
GAME_OVER_COLOR = (255, 90, 90)

# Movement timing (game ticks per second)
TICKS_PER_SECOND = 8
MOVE_EVENT = pygame.USEREVENT + 1
MOVE_INTERVAL_MS = int(1000 / TICKS_PER_SECOND)

# Directions as (dx, dy) on the grid
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def handle_events(direction, game_over=False):
    """Process input events; return (keep_running, new_direction, restart)."""
    new_dir = direction
    keep_running = True
    restart = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                keep_running = False
            if game_over:
                if event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                    restart = True
            else:
                # Arrow keys
                if event.key == pygame.K_UP:
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
    return keep_running, new_dir, restart


def choose_direction(current, attempted):
    """Prevent reversing into itself by disallowing exact opposite direction."""
    if (current[0] + attempted[0] == 0) and (current[1] + attempted[1] == 0):
        return current
    return attempted


def wrap_pos(x, y):
    """Wrap position around screen grid (toroidal wrapping)."""
    return x % GRID_COLS, y % GRID_ROWS


def move_snake(snake, direction, grow=False):
    """Move snake: returns new list of segments; if grow, keep tail."""
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = wrap_pos(head_x + dx, head_y + dy)
    if grow:
        return [new_head] + snake
    return [new_head] + snake[:-1]


def spawn_food(occupied):
    """Spawn food at a random free cell not in occupied set."""
    free_cells = [(x, y) for x in range(GRID_COLS) for y in range(GRID_ROWS) if (x, y) not in occupied]
    if not free_cells:
        return None
    return random.choice(free_cells)


def draw_cell(surface, cell, color):
    x, y = cell
    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(surface, color, rect)


def render(screen, snake, food, score, font, game_over=False):
    screen.fill(BG_COLOR)
    # Draw food
    if food is not None:
        draw_cell(screen, food, FOOD_COLOR)
    # Draw body
    for segment in snake[1:]:
        draw_cell(screen, segment, SNAKE_COLOR)
    # Draw head
    draw_cell(screen, snake[0], HEAD_COLOR)

    # HUD: score top-left
    hud = font.render(f"Score: {score}", True, HUD_COLOR)
    screen.blit(hud, (8, 6))

    if game_over:
        over_text = font.render("Game Over - Press R/Enter/Space", True, GAME_OVER_COLOR)
        rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(over_text, rect)

    pygame.display.flip()


def init_game_state():
    # Initialize snake centered, length 4, heading right
    start_x, start_y = GRID_COLS // 2, GRID_ROWS // 2
    snake = [
        (start_x, start_y),
        (start_x - 1, start_y),
        (start_x - 2, start_y),
        (start_x - 3, start_y),
    ]
    direction = RIGHT
    food = spawn_food(set(snake))
    score = 0
    return snake, direction, food, score


def main() -> int:
    pygame.init()
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 24)

        snake, direction, food, score = init_game_state()
        game_over = False

        # Timed movement
        pygame.time.set_timer(MOVE_EVENT, MOVE_INTERVAL_MS)

        running = True
        while running:
            running, direction, restart = handle_events(direction, game_over)
            if restart and game_over:
                snake, direction, food, score = init_game_state()
                game_over = False

            # Tick-based update
            for event in pygame.event.get([MOVE_EVENT]):
                if event.type == MOVE_EVENT and not game_over:
                    next_head = wrap_pos(snake[0][0] + direction[0], snake[0][1] + direction[1])
                    ate = (food is not None) and (next_head == food)
                    new_snake = move_snake(snake, direction, grow=ate)

                    # Self-collision: head overlaps any body segment
                    if next_head in new_snake[1:]:
                        game_over = True
                    else:
                        snake = new_snake
                        if ate:
                            score += 1
                            food = spawn_food(set(snake))

            # Render
            render(screen, snake, food, score, font, game_over)

            clock.tick(FPS)
        return 0
    finally:
        pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
