import sys
import pygame

# Window settings
WIDTH, HEIGHT = 640, 480
TITLE = "Snake"
FPS = 12
BG_COLOR = (0, 0, 0)


def handle_events() -> bool:
    """Process input events. Return False to request exit."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return False
    return True


def main() -> int:
    pygame.init()
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()

        running = True
        while running:
            running = handle_events()

            # Update world (none yet)

            # Render
            screen.fill(BG_COLOR)
            pygame.display.flip()

            clock.tick(FPS)
        return 0
    finally:
        pygame.quit()


if __name__ == "__main__":
    sys.exit(main())
