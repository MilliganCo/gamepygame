import pygame
import math

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.icon = 'E'

    def move_towards_player(self, player):
        """Двигается к игроку, останавливается рядом"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        # Двигаемся только если расстояние больше 1
        if distance > 1:
            self.x += int(round(dx / distance))
            self.y += int(round(dy / distance))
