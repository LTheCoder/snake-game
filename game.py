import os
import random
import pygame
import sys
from fruit import Fruit
from snake import Snake
from dotenv import load_dotenv

from special_fruit import SpecialFruit


load_dotenv()

CELL_SIZE = int(os.getenv("CELL_SIZE", 15))
GRID_WIDTH = int(os.getenv("GRID_WIDTH", 40))
GRID_HEIGHT = int(os.getenv("GRID_HEIGHT", 30))
FRAMERATE = int(os.getenv("FRAMERATE", 60))
SNAKE_SPEED = int(os.getenv("SNAKE_SPEED_MS", 100))

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        grid_center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = Snake(grid_center)
        self.fruit = Fruit([GRID_WIDTH, GRID_HEIGHT])
        self.special_fruit = None
        self.score = 0

    def draw_board(self):
        colors = [(170, 215, 81), (162, 209, 73)]
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                color = colors[(row + col) % 2]
                rect = pygame.Rect(col * CELL_SIZE, row *
                                   CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.window, color, rect)

    def run(self):
        while True:
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(pygame.Vector2(0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(pygame.Vector2(0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(pygame.Vector2(-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(pygame.Vector2(1, 0))

            if now - self.snake.last_move_time >= SNAKE_SPEED:
                self.snake.update()
                self.snake.last_move_time = now

            head = self.snake.body[0]

            interpolation = min(
                (now - self.snake.last_move_time) / SNAKE_SPEED, 1.0)

            # check if head touches body
            if head in self.snake.body[1:]:
                print("Game Over: You ran into yourself!")
                pygame.quit()
                sys.exit()

            # winning case. if snake size is board size
            if len(self.snake.body) >= GRID_HEIGHT * GRID_WIDTH:
                print("you won!")
                pygame.quit()
                sys.exit()

            # check if snake eat fruit
            if head == self.fruit.position:
                self.snake.set_grow()
                self.fruit.generate_new_position()
                self.score += 1

            # check if snake touches the "wall".
            if (
                head.x < 0 or head.y < 0 or
                head.x >= GRID_WIDTH or head.y >= GRID_HEIGHT
            ):
                print("Game Over: Hit the wall!")
                pygame.quit()
                sys.exit()

            # genrates a speical fruit with chance of 1 to 1000
            if random.random() < 0.001 and self.special_fruit is None:
                self.special_fruit = SpecialFruit([GRID_WIDTH, GRID_HEIGHT])

            if self.special_fruit:
                if self.snake.body[0] == self.special_fruit.position:
                    self.snake.set_grow(segments=3)
                    self.score += 5
                    self.special_fruit = None
                elif self.special_fruit.is_expired():
                    self.special_fruit = None

            self.draw_board()
            self.fruit.draw(self.window)
            if self.special_fruit:
                self.special_fruit.draw(self.window)
            self.snake.draw(self.window, interpolation)

            pygame.display.flip()
            self.clock.tick(FRAMERATE)
