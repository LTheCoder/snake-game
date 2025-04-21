import pygame
from dotenv import load_dotenv
import os


load_dotenv()

CELL_SIZE = int(os.getenv("CELL_SIZE", 15))

# Constants for snake properties
SNAKE_COLOR = (0, 255, 0)


class Snake:
    def __init__(self, position):
        """Initialize the snake with a starting position."""
        if not isinstance(position, (list, tuple)) or len(position) != 2:
            raise ValueError(
                "Position must be a list or tuple with two elements.")

        self.last_move_time = pygame.time.get_ticks()
        self.body = [pygame.Vector2(position)]
        self.previous_body = list(self.body)
        self.direction = pygame.Vector2(1, 0)
        self.color = SNAKE_COLOR
        self.grow_segments = 0
        self.is_direction_changed = False

    def set_grow(self, segments=1):
        """Increase the number of segments the snake will grow."""
        self.grow_segments += segments

    def update(self):
        """Update the snake's position and handle growth."""
        self.previous_body = list(self.body)
        head = self.body[0] + self.direction
        self.body.insert(0, head)

        if self.grow_segments > 0:
            self.grow_segments -= 1
        else:
            self.body.pop()

        self.is_direction_changed = False

    def handle_input(self, event):
        """Handle user input to change the snake's direction."""
        if event.type != pygame.KEYDOWN:
            return

        new_direction = None
        if event.key == pygame.K_UP:
            new_direction = pygame.Vector2(0, -1)
        elif event.key == pygame.K_DOWN:
            new_direction = pygame.Vector2(0, 1)
        elif event.key == pygame.K_LEFT:
            new_direction = pygame.Vector2(-1, 0)
        elif event.key == pygame.K_RIGHT:
            new_direction = pygame.Vector2(1, 0)

        if new_direction and self.is_valid_direction(new_direction) and not self.is_direction_changed:
            self.direction = new_direction
            self.is_direction_changed = True

    def is_valid_direction(self, new_direction):
        """Check if the new direction is valid (not opposite to the current direction)."""
        return (new_direction + self.direction) != pygame.Vector2(0, 0)

    def draw(self, surface, interpolation):
        """Draw the snake on the given surface with interpolation for smooth movement."""
        for prev, current in zip(self.previous_body, self.body):
            # Interpolate between the previous and current positions for smooth movement
            interp_pos = prev.lerp(current, interpolation)
            rect = pygame.Rect(
                int(interp_pos.x * CELL_SIZE),
                int(interp_pos.y * CELL_SIZE),
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(surface, self.color, rect)
