import pygame
import sys
from snake import Snake 

GRID_SIZE = 50, 30 
CELL_SIZE = 15
WINDOW_WIDTH = GRID_SIZE[0] * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE[1] * CELL_SIZE

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        grid_center = (GRID_SIZE[0] // 2, GRID_SIZE[1] // 2)
        self.snake = Snake(grid_center)

    def draw_board(self):
        colors = [(170, 215, 81), (162, 209, 73)] 
        for row in range(GRID_SIZE[1]):
            for col in range(GRID_SIZE[0]):
                color = colors[(row + col) % 2]
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.window, color, rect)

    
    def run(self):
        while True:
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

            self.snake.move()
            self.draw_board()
            self.snake.draw(self.window)

            pygame.display.flip()
            self.clock.tick(10)
