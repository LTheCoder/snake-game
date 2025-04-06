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

    def update(self):
        self.previous_body = list(self.body)
        head = self.body[0] + self.direction
        self.body.insert(0, head)
        self.body.pop()

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
