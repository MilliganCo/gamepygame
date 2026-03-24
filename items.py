import pygame
import random

class Item:
    def __init__(self, x, y, item_type="key"):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.color = (255, 255, 0)  # Жёлтый (цвет для ключа)
        self.item_type = item_type  # Тип предмета (например, ключ)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, player):
        # Проверяем столкновение игрока с предметом
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        item_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(item_rect)
