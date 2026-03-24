import pygame
import random
from enemy import Enemy  # Можно использовать базовый класс врага как основу

# Базовый класс босса
class Boss:
    def __init__(self, x, y, width=64, height=64, hp=100, speed=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 0, 0)  # Красный цвет
        self.hp = hp
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print("Boss defeated!")
            return True  # Убит
        return False

    def update(self, player):
        pass  # Логика поведения босса, определяемая в дочерних классах


# Босс, который стреляет снарядами
class ShootingBoss(Boss):
    def __init__(self, x, y, projectile_color=(255, 255, 0)):
        super().__init__(x, y, hp=150)
        self.projectiles = []
        self.projectile_color = projectile_color

    def update(self, player):
        # Выпускаем снаряд каждые несколько секунд
        if random.random() < 0.01:  # Вероятность выпуска снаряда
            self.projectiles.append({"x": self.x + self.width // 2, "y": self.y + self.height // 2, "speed": 5})

        # Обновляем снаряды
        for projectile in self.projectiles[:]:
            projectile["y"] += projectile["speed"]
            if projectile["y"] > 600:  # Удаляем снаряды, если они уходят за экран
                self.projectiles.remove(projectile)

    def draw(self, screen):
        super().draw(screen)
        # Отрисовываем снаряды
        for projectile in self.projectiles:
            pygame.draw.circle(screen, self.projectile_color, (int(projectile["x"]), int(projectile["y"])), 5)


# Босс ближнего боя
class MeleeBoss(Boss):
    def update(self, player):
        # Двигается к игроку
        if self.x < player.x:
            self.x += self.speed
        if self.x > player.x:
            self.x -= self.speed
        if self.y < player.y:
            self.y += self.speed
        if self.y > player.y:
            self.y -= self.speed


# Босс, вызывающий мелких врагов
class SummoningBoss(Boss):
    def __init__(self, x, y):
        super().__init__(x, y, hp=200)
        self.minions = []  # Список вызванных миньонов

    def update(self, player):
        # Вызывает миньонов с определённой вероятностью
        if random.random() < 0.01 and len(self.minions) < 5:
            self.minions.append(Enemy(random.randint(0, 800), random.randint(0, 600)))

        # Обновляет миньонов
        for minion in self.minions:
            minion.move_towards_player(player)

    def draw(self, screen):
        super().draw(screen)
        for minion in self.minions:
            minion.draw(screen)
