import os
import random
import pygame
import sys
from fruit import Fruit
from snake import Snake
from dotenv import load_dotenv

from special_fruit import SpecialFruit
from enum import Enum

load_dotenv()

CELL_SIZE = int(os.getenv("CELL_SIZE", 15))
GRID_WIDTH = int(os.getenv("GRID_WIDTH", 40))
GRID_HEIGHT = int(os.getenv("GRID_HEIGHT", 30))
FRAMERATE = int(os.getenv("FRAMERATE", 60))
SNAKE_SPEED = int(os.getenv("SNAKE_SPEED_MS", 100))

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE


class GameStatus(str, Enum):
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    MENU = "MENU"


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
        self.state = GameStatus.MENU  # "MENU", "PLAYING", "GAME_OVER"

    def draw_board(self):
        colors = [(170, 215, 81), (162, 209, 73)]
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                color = colors[(row + col) % 2]
                rect = pygame.Rect(col * CELL_SIZE, row *
                                   CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.window, color, rect)

    def draw_menu(self):
        self.window.fill((30, 30, 30))
        font = pygame.font.SysFont(None, 60)
        small_font = pygame.font.SysFont(None, 30)

        title = font.render("Snake Game", True, (0, 255, 0))
        start = small_font.render(
            "Press SPACE to Start", True, (200, 200, 200))

        self.window.blit(title, (WINDOW_WIDTH // 2 -
                         title.get_width() // 2, 150))
        self.window.blit(start, (WINDOW_WIDTH // 2 -
                         start.get_width() // 2, 250))

    def draw_game_over(self):
        self.window.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 60)
        small_font = pygame.font.SysFont(None, 30)

        game_over = font.render("Game Over", True, (255, 0, 0))
        score_text = small_font.render(
            f"Final Score: {self.score}", True, (255, 255, 255))
        restart = small_font.render(
            "Press R to Restart", True, (200, 200, 200))

        menu = small_font.render(
            "Press M to go to Menu", True, (200, 200, 200))
        self.window.blit(menu, (WINDOW_WIDTH // 2 -
                         menu.get_width() // 2, 300))
        self.window.blit(game_over, (WINDOW_WIDTH // 2 -
                         game_over.get_width() // 2, 150))
        self.window.blit(score_text, (WINDOW_WIDTH // 2 -
                         score_text.get_width() // 2, 220))
        self.window.blit(restart, (WINDOW_WIDTH // 2 -
                         restart.get_width() // 2, 270))

    def reset_game(self):
        self.snake = Snake((GRID_WIDTH // 2, GRID_HEIGHT // 2))
        self.fruit = Fruit([GRID_WIDTH, GRID_HEIGHT])
        self.special_fruit = None
        self.score = 0

    def update_game(self):
        now = pygame.time.get_ticks()

        if now - self.snake.last_move_time >= SNAKE_SPEED:
            self.snake.update()
            self.snake.last_move_time = now

        head = self.snake.body[0]

        interpolation = min(
            (now - self.snake.last_move_time) / SNAKE_SPEED, 1.0)

        # check if head touches body
        if head in self.snake.body[1:]:
            self.state = GameStatus.GAME_OVER

        # winning case. if snake size is board size
        if len(self.snake.body) >= GRID_HEIGHT * GRID_WIDTH:
            self.state = GameStatus.MENU
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
            self.state = GameStatus.GAME_OVER
        # generates a special fruit with chance of 1 to 1000
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

        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(text, (10, 10))

        self.clock.tick(FRAMERATE)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.state == "MENU" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = "PLAYING"
                elif self.state == "GAME_OVER" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                    self.state = "PLAYING"
                elif self.state == "GAME_OVER" and event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.reset_game()
                    self.state = "MENU"
                elif self.state == "PLAYING":
                    self.snake.handle_input(event)

            if self.state == "PLAYING":
                self.update_game()
            elif self.state == "MENU":
                self.draw_menu()
            elif self.state == "GAME_OVER":
                self.draw_game_over()

            pygame.display.flip()
