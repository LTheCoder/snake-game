from fruit import Fruit
import pygame

# Constants for special fruit properties
SPECIAL_FRUIT_COLOR = (255, 215, 0)
SPECIAL_FRUIT_DURATION = 4000

class SpecialFruit(Fruit):
    """Represents a special fruit with a limited duration."""

    def __init__(self, grid_size):
        if not isinstance(grid_size, (list, tuple)) or len(grid_size) != 2:
            raise ValueError("Grid size must be a list or tuple with two elements.")

        super().__init__(grid_size, color=SPECIAL_FRUIT_COLOR)
        self.spawn_time = pygame.time.get_ticks()
        self.duration = SPECIAL_FRUIT_DURATION

    def has_expired(self):
        """Check if the special fruit has expired based on its duration."""
        return pygame.time.get_ticks() - self.spawn_time > self.duration