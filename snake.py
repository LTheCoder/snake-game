import pygame
from dotenv import load_dotenv
import os


load_dotenv()

CELL_SIZE = int(os.getenv("CELL_SIZE", 20))


class Snake:
    def __init__(self, position):
        self.body = [pygame.Vector2(position)]
        self.direction = pygame.Vector2(1, 0)
        self.color = (0, 255, 0)

    def move(self):
        head = self.body[0] + self.direction
        self.body.insert(0, head)
        self.body.pop()

    def change_direction(self, direction):
        if (direction + self.direction) != pygame.Vector2(0, 0):
            self.direction = direction

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(
                int(segment.x * CELL_SIZE),
                int(segment.y * CELL_SIZE),
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(surface, self.color, rect)
