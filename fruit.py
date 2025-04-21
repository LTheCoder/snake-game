import random
import pygame
import os
from dotenv import load_dotenv

load_dotenv()

CELL_SIZE = int(os.getenv("CELL_SIZE", 15))
if CELL_SIZE <= 0:
    raise ValueError("CELL_SIZE must be a positive integer.")

# Constants for fruit properties
DEFAULT_FRUIT_COLOR = (255, 0, 0)

class Fruit:
    """Represents a fruit object in the game."""

    def __init__(self, grid_size, color=DEFAULT_FRUIT_COLOR):
        """Initialize the fruit with a grid size and optional color."""
        if not isinstance(grid_size, (list, tuple)) or len(grid_size) != 2:
            raise ValueError("Grid size must be a list or tuple with two positive integers.")
        if not all(isinstance(dim, int) and dim > 0 for dim in grid_size):
            raise ValueError("Grid size dimensions must be positive integers.")

        self.color = color
        self.grid_size = grid_size
        self.position = self.random_position()

    def generate_new_position(self):
        """Generate a new random position for the fruit."""
        self.position = self.random_position()

    def random_position(self):
        """Generate a random position within the grid size."""
        x = random.randint(0, self.grid_size[0] - 1)
        y = random.randint(0, self.grid_size[1] - 1)
        return pygame.Vector2(x, y)

    def draw(self, surface):
        """Draw the fruit on the given surface."""
        center = (
            int(self.position.x * CELL_SIZE + CELL_SIZE // 2),
            int(self.position.y * CELL_SIZE + CELL_SIZE // 2)
        )
        radius = CELL_SIZE // 2
        pygame.draw.circle(surface, self.color, center, radius)
