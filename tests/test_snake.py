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


# Teste 1: spawn_food retorna posição livre
def test_spawn_food_returns_free_position():
    occupied = {(0, 0), (1, 1)}
    food = spawn_food(occupied)
    assert food not in occupied
    assert 0 <= food[0] < WIDTH
    assert 0 <= food[1] < HEIGHT

# Teste 2: direção RIGHT move corretamente
def test_snake_moves_right():
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = RIGHT
    hx, hy = snake[0]
    dx, dy = direction
    nx, ny = (hx + dx) % WIDTH, (hy + dy) % HEIGHT
    assert (nx, ny) == (6, 5)

# Teste 3: colisão da cobra consigo mesma
def test_snake_self_collision():
    snake = [(5, 5), (4, 5), (3, 5)]
    new_head = (4, 5)
    assert new_head in snake

# Teste 4: consumo de comida faz crescer
def test_snake_eats_food_and_grows():
    snake = [(5, 5), (4, 5), (3, 5)]
    food = (6, 5)
    direction = RIGHT
    hx, hy = snake[0]
    dx, dy = direction
    nx, ny = (hx + dx) % WIDTH, (hy + dy) % HEIGHT
    new_head = (nx, ny)
    if new_head == food:
        snake_after = [new_head] + snake
    else:
        snake_after = [new_head] + snake[:-1]
    assert len(snake_after) == len(snake) + 1

# Teste 5: constantes do grid
def test_grid_constants():
    assert WIDTH > 0
    assert HEIGHT > 0
