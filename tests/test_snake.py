"""
Testes unitários para o jogo Snake
"""
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import curses

from snake.text_snake import (DIRECTIONS, DOWN, HEIGHT, LEFT, RIGHT, UP, WIDTH,
                              spawn_food)


class TestSpawnFood:
    """Testa a função spawn_food"""

    def test_spawn_food_empty_grid(self):
        """Testa spawn_food em um grid vazio"""
        occupied = set()
        food = spawn_food(occupied)

        assert 0 <= food[0] < WIDTH
        assert 0 <= food[1] < HEIGHT

        assert food not in occupied

    def test_spawn_food_with_occupied_positions(self):
        """Testa spawn_food com posições ocupadas"""
        occupied = {(0, 0), (1, 0), (2, 0)}
        food = spawn_food(occupied)

        assert 0 <= food[0] < WIDTH
        assert 0 <= food[1] < HEIGHT

        assert food not in occupied

    def test_spawn_food_almost_full_grid(self):
        """Testa spawn_food quando quase todo o grid está ocupado"""
        occupied = set()
        for x in range(WIDTH):
            for y in range(HEIGHT):
                occupied.add((x, y))

        free_position = (5, 5)
        occupied.remove(free_position)

        food = spawn_food(occupied)

        assert food == free_position

    @patch("random.choice")
    def test_spawn_food_randomness(self, mock_choice):
        """Testa se spawn_food usa random.choice corretamente"""
        occupied = {(0, 0)}
        expected_food = (10, 10)
        mock_choice.return_value = expected_food

        food = spawn_food(occupied)

        mock_choice.assert_called_once()
        assert food == expected_food


class TestDirections:
    """Testa as constantes e mapeamentos de direções"""

    def test_direction_constants(self):
        """Testa se as constantes de direção estão corretas"""
        assert UP == (0, -1)
        assert DOWN == (0, 1)
        assert LEFT == (-1, 0)
        assert RIGHT == (1, 0)

    def test_directions_mapping(self):
        """Testa o mapeamento de teclas para direções"""

        assert DIRECTIONS[curses.KEY_UP] == UP
        assert DIRECTIONS[curses.KEY_DOWN] == DOWN
        assert DIRECTIONS[curses.KEY_LEFT] == LEFT
        assert DIRECTIONS[curses.KEY_RIGHT] == RIGHT

        assert DIRECTIONS[ord("w")] == UP
        assert DIRECTIONS[ord("s")] == DOWN
        assert DIRECTIONS[ord("a")] == LEFT
        assert DIRECTIONS[ord("d")] == RIGHT

    def test_opposite_directions(self):
        """Testa se direções opostas se cancelam"""

        assert (UP[0] + DOWN[0], UP[1] + DOWN[1]) == (0, 0)
        assert (LEFT[0] + RIGHT[0], LEFT[1] + RIGHT[1]) == (0, 0)


class TestGameLogic:
    """Testa a lógica básica do jogo"""

    def test_snake_movement_right(self):
        """Testa movimento da cobra para a direita"""
        snake = [(5, 5), (4, 5), (3, 5)]
        direction = RIGHT

        hx, hy = snake[0]
        dx, dy = direction
        nx, ny = (hx + dx) % WIDTH, (hy + dy) % HEIGHT
        new_head = (nx, ny)

        expected_head = (6, 5)
        assert new_head == expected_head

    def test_snake_movement_wrapping(self):
        """Testa se a cobra passa pelas bordas (wrapping)"""

        snake = [(WIDTH - 1, 5)]
        direction = RIGHT
        hx, hy = snake[0]
        dx, dy = direction
        nx, ny = (hx + dx) % WIDTH, (hy + dy) % HEIGHT
        new_head = (nx, ny)

        assert new_head == (0, 5)  # deve wrap para x=0

        snake = [(5, HEIGHT - 1)]
        direction = DOWN
        hx, hy = snake[0]
        dx, dy = direction
        nx, ny = (hx + dx) % WIDTH, (hy + dy) % HEIGHT
        new_head = (nx, ny)

        assert new_head == (5, 0)  # deve wrap para y=0

    def test_snake_collision_detection(self):
        """Testa detecção de colisão da cobra consigo mesma"""
        snake = [(5, 5), (4, 5), (3, 5), (2, 5)]
        new_head = (4, 5)

        # Simula colisão
        collision = new_head in snake
        assert collision is True

        # Testa posição livre
        new_head = (6, 5)
        collision = new_head in snake
        assert collision is False

    def test_food_consumption(self):
        """Testa consumo de comida e crescimento da cobra"""
        snake = [(5, 5), (4, 5), (3, 5)]
        food = (6, 5)
        initial_length = len(snake)

        # Simula movimento em direção à comida
        direction = RIGHT
        hx, hy = snake[0]
        dx, dy = direction
        nx, ny = (hx + dx) % WIDTH, (hy + dy) % HEIGHT
        new_head = (nx, ny)

        # Verifica se nova cabeça é a comida
        food_eaten = new_head == food
        assert food_eaten is True

        # Simula crescimento (adiciona cabeça sem remover cauda)
        if food_eaten:
            snake_after = [new_head] + snake
        else:
            snake_after = [new_head] + snake[:-1]

        # Cobra deve ter crescido
        assert len(snake_after) == initial_length + 1
        assert snake_after[0] == food


class TestGameConstants:
    """Testa constantes do jogo"""

    def test_grid_dimensions(self):
        """Testa se as dimensões do grid são válidas"""
        assert WIDTH > 0
        assert HEIGHT > 0
        assert isinstance(WIDTH, int)
        assert isinstance(HEIGHT, int)

    def test_character_constants(self):
        """Testa se os caracteres do jogo estão definidos"""
        from snake.text_snake import (EMPTY_CHAR, FOOD_CHAR, HEAD_CHAR,
                                      SNAKE_CHAR)

        assert isinstance(SNAKE_CHAR, str)
        assert isinstance(FOOD_CHAR, str)
        assert isinstance(EMPTY_CHAR, str)
        assert isinstance(HEAD_CHAR, str)

        # Verifica se são caracteres únicos
        assert len(SNAKE_CHAR) == 1
        assert len(FOOD_CHAR) == 1
        assert len(EMPTY_CHAR) == 1
        assert len(HEAD_CHAR) == 1


if __name__ == "__main__":
    pytest.main([__file__])
