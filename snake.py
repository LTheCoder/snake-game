import pygame
from dotenv import load_dotenv
import os


load_dotenv()

CELL_SIZE = int(os.getenv("CELL_SIZE", 15))


class Snake:
    def __init__(self, position):
        self.last_move_time = pygame.time.get_ticks()
        self.body = [pygame.Vector2(position)]
        self.previous_body = list(self.body)
        self.direction = pygame.Vector2(1, 0)
        self.color = (0, 255, 0)
        self.grow_segments = 0

    def set_grow(self, segments=1):
        self.grow_segments += segments

    def update(self):
        self.previous_body = list(self.body)
        head = self.body[0] + self.direction
        self.body.insert(0, head)

        if self.grow_segments > 0:
            self.grow_segments -= 1
        else:
            self.body.pop()

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP and self.direction != pygame.Vector2(0, 1):
            self.direction = pygame.Vector2(0, -1)
        elif event.key == pygame.K_DOWN and self.direction != pygame.Vector2(0, -1):
            self.direction = pygame.Vector2(0, 1)
        elif event.key == pygame.K_LEFT and self.direction != pygame.Vector2(1, 0):
            self.direction = pygame.Vector2(-1, 0)
        elif event.key == pygame.K_RIGHT and self.direction != pygame.Vector2(-1, 0):
            self.direction = pygame.Vector2(1, 0)

    def change_direction(self, direction):
        if (direction + self.direction) != pygame.Vector2(0, 0):
            self.direction = direction

    def draw(self, surface, interpolation):
        for prev, current in zip(self.previous_body, self.body):
            interp_pos = prev.lerp(current, interpolation)
            rect = pygame.Rect(
                int(interp_pos.x * CELL_SIZE),
                int(interp_pos.y * CELL_SIZE),
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(surface, self.color, rect)
