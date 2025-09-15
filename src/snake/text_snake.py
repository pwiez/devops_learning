import curses
import random
import time

WIDTH, HEIGHT = 20, 12  # grid size
SNAKE_CHAR = 'O'
FOOD_CHAR = '*'
EMPTY_CHAR = ' '
HEAD_CHAR = '@'

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = {curses.KEY_UP: UP, curses.KEY_DOWN: DOWN, curses.KEY_LEFT: LEFT, curses.KEY_RIGHT: RIGHT,
              ord('w'): UP, ord('s'): DOWN, ord('a'): LEFT, ord('d'): RIGHT}


def spawn_food(occupied):
    free = [(x, y) for x in range(WIDTH) for y in range(HEIGHT) if (x, y) not in occupied]
    return random.choice(free)


def draw_grid(stdscr, snake, food, score):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Score: {score}")
    for y in range(HEIGHT):
        row = ''
        for x in range(WIDTH):
            if (x, y) == snake[0]:
                row += HEAD_CHAR
            elif (x, y) in snake[1:]:
                row += SNAKE_CHAR
            elif (x, y) == food:
                row += FOOD_CHAR
            else:
                row += EMPTY_CHAR
        stdscr.addstr(y + 1, 0, row)
    stdscr.addstr(HEIGHT + 2, 0, "Controls: Arrow keys or WASD to move, Q to quit")
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(150)
    snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - 1, HEIGHT // 2), (WIDTH // 2 - 2, HEIGHT // 2)]
    direction = RIGHT
    food = spawn_food(set(snake))
    score = 0
    game_over = False

    while not game_over:
        draw_grid(stdscr, snake, food, score)
        key = stdscr.getch()
        if key in DIRECTIONS:
            new_dir = DIRECTIONS[key]
            # Prevent reversing
            if (direction[0] + new_dir[0], direction[1] + new_dir[1]) != (0, 0):
                direction = new_dir
        elif key in [ord('q'), ord('Q')]:
            break
        # Move snake
        hx, hy = snake[0]
        dx, dy = direction
        nx, ny = (hx + dx) % WIDTH, (hy + dy) % HEIGHT
        new_head = (nx, ny)
        if new_head in snake:
            draw_grid(stdscr, snake, food, score)
            stdscr.addstr(HEIGHT + 3, 0, "Game Over! Press any key to exit.")
            stdscr.nodelay(False)
            stdscr.getch()
            break
        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = spawn_food(set(snake))
        else:
            snake.pop()

if __name__ == "__main__":
    curses.wrapper(main)
