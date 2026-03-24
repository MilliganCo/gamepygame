import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.icon = '@'  # ASCII-иконка игрока
        self.inventory = [["" for _ in range(4)] for _ in range(4)]  # Сетка 4x4
        self.skills = []  # Навыки игрока
        self.hp = 100  # Здоровье игрока
        self.attack_damage = 10  # Урон игрока
        self.speed = 1  # Скорость перемещения

    def draw(self, game_map):
        """Отображает игрока на карте"""
        game_map[self.y][self.x] = self.icon

    def handle_keys(self, key, game_map):
        """Обрабатывает ввод клавиш для перемещения с проверкой карты"""
        if key == pygame.K_w and game_map[self.y - self.speed][self.x] != '#':  # Вверх
            self.y = max(self.y - self.speed, 1)
        elif key == pygame.K_s and game_map[self.y + self.speed][self.x] != '#':  # Вниз
            self.y = min(self.y + self.speed, len(game_map) - 2)
        elif key == pygame.K_a and game_map[self.y][self.x - self.speed] != '#':  # Влево
            self.x = max(self.x - self.speed, 1)
        elif key == pygame.K_d and game_map[self.y][self.x + self.speed] != '#':  # Вправо
            self.x = min(self.x + self.speed, len(game_map[0]) - 2)

    def add_to_inventory(self, item_type):
        """Добавляет предмет в первый свободный слот инвентаря"""
        for row in range(4):
            for col in range(4):
                if self.inventory[row][col] == "":
                    self.inventory[row][col] = item_type
                    return True
        print("Inventory is full!")
        return False  # Инвентарь полон

    def take_damage(self, damage):
        """Уменьшает здоровье игрока"""
        self.hp -= damage
        if self.hp <= 0:
            print("Player has been defeated!")

    def draw_inventory(screen, player, font):
        """Отображает инвентарь в игровом окне"""
        inventory_width, inventory_height = 300, 300
        inventory_x = (WINDOW_WIDTH - inventory_width) // 2
        inventory_y = (WINDOW_HEIGHT - inventory_height) // 2

        # Рисуем фон инвентаря
        pygame.draw.rect(screen, COLOR_CHAT_BG, (inventory_x, inventory_y, inventory_width, inventory_height))

        # Отображаем сетку инвентаря
        cell_size = inventory_width // 4
        for row in range(4):
            for col in range(4):
                x = inventory_x + col * cell_size
                y = inventory_y + row * cell_size
                pygame.draw.rect(screen, COLOR_TEXT, (x, y, cell_size, cell_size), 2)
                item = player.inventory[row][col]
                if item:
                    item_text = font.render(item, True, COLOR_CHAT_TEXT)
                    screen.blit(item_text, (x + 5, y + 5))

    def display_inventory(self):
        """Отображает инвентарь и навыки"""
        print("\n" + "=" * 20 + " INVENTORY " + "=" * 20)
        for row in self.inventory:
            print(" | ".join([slot if slot else "EMPTY" for slot in row]))
        print("=" * 50)
        print("Skills:")
        for i, skill in enumerate(self.skills, start=1):
            print(f"{i}. {skill}")
        print("=" * 50)

    def choose_skill(self):
        """Позволяет игроку выбрать новый навык"""
        options = ["Speed Boost", "Melee Damage", "Health Boost"]
        print("Choose a skill:")
        for i, skill in enumerate(options):
            print(f"{i + 1}. {skill}")

        choice = int(input("Enter skill number: ")) - 1
        if 0 <= choice < len(options):
            self.skills.append(options[choice])
            print(f"Skill acquired: {options[choice]}")
            if options[choice] == "Speed Boost":
                self.speed += 1
            elif options[choice] == "Melee Damage":
                self.attack_damage += 5
            elif options[choice] == "Health Boost":
                self.hp += 20
