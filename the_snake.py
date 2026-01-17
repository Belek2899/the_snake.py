"""Игра Змейка на Pygame."""

import random

import pygame as pg

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_CENTER = (
    SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,
    SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE,
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

# Инициализация pygame
# pylint: disable=no-member
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """
        Инициализирует игровой объект.

        Args:
            body_color: Цвет объекта.
        """
        self.position = BOARD_CENTER
        self.body_color = body_color

    def draw_cell(self, position, surface):
        """Отрисовывает одну ячейку."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        raise NotImplementedError('Метод draw должен быть переопределен')


class Apple(GameObject):
    """Класс яблока в игре."""

    def __init__(self, body_color=APPLE_COLOR,
                 occupied_positions=(BOARD_CENTER,)):
        """
        Инициализирует яблоко с заданным цветом и случайной позицией.
        Args:
            body_color: Цвет яблока (по умолчанию красный).
            occupied_positions: Занятые позиции, которых нужно избегать.
        """
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайное положение яблока на поле."""
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position, surface)


class Snake(GameObject):
    """Класс змейки в игре."""

    def __init__(self, body_color=SNAKE_COLOR):
        """
        Инициализирует змейку в начальном состоянии.
        Args:
            body_color: Цвет змейки (по умолчанию зелёный).
        """
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки, добавляя новую голову."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            self.draw_cell(position, surface)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def check_collision(self):
        """Проверяет столкновение змейки с самой собой."""
        head = self.get_head_position()
        return head in self.positions[1:]


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления движения.

    Args:
        snake: Игровой объект (змейка), направление которого
              нужно изменить.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:  # pylint: disable=no-member
            pg.quit()  # pylint: disable=no-member
            raise SystemExit
        elif event.type == pg.KEYDOWN:  # pylint: disable=no-member
            # pylint: disable=no-member
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            # pylint: disable=no-member
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            # pylint: disable=no-member
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            # pylint: disable=no-member
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.check_collision():
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)

        pg.display.update()


if __name__ == '__main__':
    main()
