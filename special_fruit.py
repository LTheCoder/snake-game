from fruit import Fruit
import pygame

class SpecialFruit(Fruit):
    def __init__(self, grid_size):
        super().__init__(grid_size, color=(255, 215, 0)) 
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 4000

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration