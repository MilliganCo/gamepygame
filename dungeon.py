import pygame
import random

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0 for _ in range(width)] for _ in range(height)]

    def generate(self):
        # Пример генерации комнаты
        for _ in range(5):  # Генерируем 5 случайных комнат
            w = random.randint(4, 8)
            h = random.randint(4, 8)
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)

            for i in range(y, y + h):
                for j in range(x, x + w):
                    self.map[i][j] = 1  # 1 означает, что клетка проходима

    def draw(self, screen, tile_size):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                color = (255, 255, 255) if tile == 1 else (0, 0, 0)
                pygame.draw.rect(screen, color, (x * tile_size, y * tile_size, tile_size, tile_size))
