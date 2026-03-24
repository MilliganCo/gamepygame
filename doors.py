import pygame

class Door:
    def __init__(self, x, y, width=32, height=64, required_item="key"):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0, 0, 255)  # Синий цвет для двери
        self.required_item = required_item  # Тип предмета, необходимого для открытия
        self.is_open = False

    def draw(self, screen):
        if not self.is_open:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def check_collision(self, player):
        # Проверяем, пересекается ли игрок с дверью
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        door_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return player_rect.colliderect(door_rect)

    def try_open(self, player):
        if self.required_item in player.inventory and player.inventory[self.required_item] > 0:
            self.is_open = True
            player.inventory[self.required_item] -= 1  # Уменьшаем количество ключей
            print(f"Door opened with {self.required_item}!")
