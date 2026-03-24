import pygame
import sys
import random
from player import Player
from boss import ShootingBoss, MeleeBoss, SummoningBoss
from enemy import Enemy
from items import Item
from doors import Door

# Настройки карты
TILE_SIZE = 32  # Размер одного символа в пикселях
MAP_WIDTH, MAP_HEIGHT = 30, 20  # Размер карты в символах
WINDOW_WIDTH, WINDOW_HEIGHT = MAP_WIDTH * TILE_SIZE, (MAP_HEIGHT + 5) * TILE_SIZE  # +5 для чата

# ASCII представление объектов
TILE_EMPTY = '.'
TILE_WALL = '#'
TILE_PLAYER = '@'
TILE_ENEMY = 'E'
TILE_BOSS = 'B'
TILE_ITEM = '*'
TILE_DOOR = 'D'
TILE_CHEST = 'C'

# Цвета
COLOR_BG = (0, 0, 0)  # Чёрный
COLOR_TEXT = (255, 255, 255)  # Белый
COLOR_CHAT_BG = (30, 30, 30)  # Тёмно-серый
COLOR_CHAT_TEXT = (200, 200, 200)  # Серый
COLOR_MENU_BG = (50, 50, 50)
COLOR_MENU_TEXT = (255, 255, 255)


def generate_map_with_corridors():
    """Создаёт карту с коридорами и пещерами"""
    # Пустая карта
    game_map = [[TILE_WALL for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    # Генерация случайных комнат
    rooms = []
    for _ in range(8):  # Генерация 8 случайных комнат
        width, height = random.randint(4, 8), random.randint(4, 8)
        x, y = random.randint(1, MAP_WIDTH - width - 1), random.randint(1, MAP_HEIGHT - height - 1)
        rooms.append((x, y, width, height))
        for i in range(y, y + height):
            for j in range(x, x + width):
                game_map[i][j] = TILE_EMPTY

    # Соединение комнат коридорами
    for i in range(len(rooms) - 1):
        x1, y1 = rooms[i][0] + rooms[i][2] // 2, rooms[i][1] + rooms[i][3] // 2
        x2, y2 = rooms[i + 1][0] + rooms[i + 1][2] // 2, rooms[i + 1][1] + rooms[i + 1][3] // 2
        while x1 != x2:
            game_map[y1][x1] = TILE_EMPTY
            x1 += 1 if x1 < x2 else -1
        while y1 != y2:
            game_map[y1][x1] = TILE_EMPTY
            y1 += 1 if y1 < y2 else -1

    # Добавление сундуков, двери и случайного босса в одну из комнат
    chest_room = random.choice(rooms)
    door_room = random.choice(rooms)
    boss_room = random.choice(rooms)
    game_map[chest_room[1] + 1][chest_room[0] + 1] = TILE_CHEST
    game_map[door_room[1] + 1][door_room[0] + 1] = TILE_DOOR

    return game_map, boss_room


def draw_map(screen, game_map, font):
    """Отображает карту на экране"""
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            text = font.render(tile, True, COLOR_TEXT)
            screen.blit(text, (x * TILE_SIZE, y * TILE_SIZE))


def draw_chat(screen, font, messages):
    """Отображает чат внизу окна"""
    chat_x = 0
    chat_y = MAP_HEIGHT * TILE_SIZE
    chat_width = WINDOW_WIDTH
    chat_height = 5 * TILE_SIZE

    # Рисуем фон чата
    pygame.draw.rect(screen, COLOR_CHAT_BG, (chat_x, chat_y, chat_width, chat_height))

    # Отображаем сообщения
    for i, message in enumerate(messages[-5:]):  # Последние 5 сообщений
        text = font.render(message, True, COLOR_CHAT_TEXT)
        screen.blit(text, (chat_x + 10, chat_y + i * TILE_SIZE))


def drop_item():
    """Определяет, какой предмет выпадет"""
    items = ["potion", "key", "bomb", "arrow", "sword"]
    return random.choice(items)


def draw_inventory(screen, player, font):
    """Отображает инвентарь в игровом окне с активным и пассивными слотами"""
    inventory_width, inventory_height = 400, 400
    inventory_x = (WINDOW_WIDTH - inventory_width) // 2
    inventory_y = (WINDOW_HEIGHT - inventory_height) // 2

    # Рисуем фон инвентаря
    pygame.draw.rect(screen, COLOR_CHAT_BG, (inventory_x, inventory_y, inventory_width, inventory_height))

    # Рисуем активный слот
    active_slot_x = inventory_x + 10
    active_slot_y = inventory_y + 10
    pygame.draw.rect(screen, COLOR_TEXT, (active_slot_x, active_slot_y, 50, 50), 2)
    active_item = player.active_item if hasattr(player, 'active_item') else None
    if active_item:
        item_text = font.render(active_item, True, COLOR_CHAT_TEXT)
        screen.blit(item_text, (active_slot_x + 5, active_slot_y + 5))

    # Рисуем пассивные слоты
    passive_slot_x = inventory_x + 70
    for i, passive_item in enumerate(getattr(player, 'passive_items', [])):
        pygame.draw.rect(screen, COLOR_TEXT, (passive_slot_x + i * 60, active_slot_y, 50, 50), 2)
        if passive_item:
            item_text = font.render(passive_item, True, COLOR_CHAT_TEXT)
            screen.blit(item_text, (passive_slot_x + i * 60 + 5, active_slot_y + 5))

    # Отображаем сетку инвентаря
    cell_size = inventory_width // 4
    for row in range(4):
        for col in range(4):
            x = inventory_x + col * cell_size
            y = inventory_y + 70 + row * cell_size
            pygame.draw.rect(screen, COLOR_TEXT, (x, y, cell_size, cell_size), 2)
            item = player.inventory[row][col]
            if item:
                item_text = font.render(item, True, COLOR_CHAT_TEXT)
                screen.blit(item_text, (x + 5, y + 5))


def choose_boss():
    """Выбирает случайного босса"""
    bosses = [ShootingBoss, MeleeBoss, SummoningBoss]
    return random.choice(bosses)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("ASCII Roguelike")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Courier", TILE_SIZE)

    # Игровые объекты
    player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)
    player.active_item = None  # Активный слот
    player.passive_items = [None, None, None, None]  # Пассивные слоты
    game_map, boss_room = generate_map_with_corridors()

    # Список врагов
    enemies = [Enemy(random.randint(1, MAP_WIDTH - 2), random.randint(1, MAP_HEIGHT - 2)) for _ in range(3)]

    # Единственный случайный босс
    boss_class = choose_boss()
    boss = boss_class(boss_room[0] + boss_room[2] // 2, boss_room[1] + boss_room[3] // 2)

    # Предметы
    items = []

    # Сообщения и статистика
    messages = []
    stats = {
        "items_collected": 0,
        "enemies_defeated": 0,
        "bosses_defeated": 0,
        "levels_completed": 1,
    }

    running = True
    show_inventory = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    show_inventory = not show_inventory
                elif event.key == pygame.K_e and player.active_item:
                    messages.append(f"Used {player.active_item}!")
                    player.use_active_item()
                elif not show_inventory:
                    player.handle_keys(event.key, game_map)

        if not show_inventory:
            player.draw(game_map)

            # Обновляем врагов
            for enemy in enemies[:]:
                enemy.move_towards_player(player)
                game_map[enemy.y][enemy.x] = TILE_ENEMY
                if player.x == enemy.x and player.y == enemy.y:
                    messages.append("Enemy hit player for 5 damage!")
                    player.take_damage(5)
                    stats["enemies_defeated"] += 1
                    dropped_item = drop_item()
                    messages.append(f"Enemy dropped {dropped_item}!")
                    items.append(Item(enemy.x, enemy.y, dropped_item))
                    enemies.remove(enemy)

            # Обновляем босса
            game_map[boss.y][boss.x] = TILE_BOSS
            if player.x == boss.x and player.y == boss.y:
                boss.hp -= player.attack_damage
                messages.append(f"Player hit boss for {player.attack_damage} damage!")
                if boss.hp <= 0:
                    messages.append("Boss defeated!")
                    stats["bosses_defeated"] += 1
                    dropped_item = "key"
                    messages.append(f"Boss dropped {dropped_item}!")
                    items.append(Item(boss.x, boss.y, dropped_item))

            # Обновляем предметы
            for item in items[:]:
                if player.x == item.x and player.y == item.y:
                    if player.add_to_inventory(item.item_type):
                        messages.append(f"Picked up {item.item_type}!")
                        stats["items_collected"] += 1
                        items.remove(item)

        # Отрисовка карты и сообщений
        screen.fill(COLOR_BG)
        if show_inventory:
            draw_inventory(screen, player, font)
        else:
            draw_map(screen, game_map, font)
            draw_chat(screen, font, messages)

        pygame.display.flip()
        clock.tick(3)  # Замедляем игру

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
