import random
import pygame
import os
from dotenv import load_dotenv

load_dotenv()

CELL_SIZE = int(os.getenv("CELL_SIZE", 15))


class Fruit:
    def __init__(self, grid_size, color=(255, 0, 0)):
        self.color = color
        self.grid_size = grid_size
        self.position = self.random_position()

    def generate_new_position(self):
        self.position = self.random_position()

    def random_position(self):
        return pygame.Vector2(
            random.randint(0, self.grid_size[0] - 1),
            random.randint(0, self.grid_size[1] - 1)
        )

    def draw(self, surface):
        center = (
            int(self.position.x * CELL_SIZE + CELL_SIZE // 2),
            int(self.position.y * CELL_SIZE + CELL_SIZE // 2)
        )
        radius = CELL_SIZE // 2
        pygame.draw.circle(surface, self.color, center, radius)
