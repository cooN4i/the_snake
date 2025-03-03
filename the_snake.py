from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Глобальная переменная - кортеж, хранящий в себе координаты середины
START_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс, являющийся родительским для классов Snake и Apple."""

    def __init__(self, body_color=None):
        self.position = START_POSITION
        self.body_color = body_color

    def draw(self):
        """Метод класса GameObject.

        Необходим для отрисовки объекта. Будет переопределяться
        в классах Snake и Apple.
        """
        pass


class Snake(GameObject):
    """Класс Snake, наследуется от класса GameObject."""

    def __init__(self, body_color=None):
        super().__init__(body_color)
        self.reset()
        self.next_direction = None
        self.last = None
        self.direction = RIGHT

    def move(self):
        """Метод, описывающий движение змейки."""
        x_coord, y_coord = self.get_head_position()
        x_direction, y_direction = self.direction
        new_head = ((x_coord + x_direction * GRID_SIZE) % SCREEN_WIDTH,
                    (y_coord + y_direction * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]
        if (len(self.positions) > self.length):
            self.positions.pop(-1)

    def update_direction(self):
        """Метод, обновляющий направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод для отрисовки змейки."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(),
                            (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, возвращающий координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод класса Snake.

        Сбрасывает все параметры змейки
        для перезапуска игры.
        """
        self.positions = [START_POSITION]
        self.length = 1
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


class Apple(GameObject):
    """Класс Snake, наследуется от класса GameObject."""

    def __init__(self, snake_coordinates=[], body_color=None):
        super().__init__(body_color)
        self.position = self.randomize_position(snake_coordinates)

    def draw(self, snake_coordinates):
        """Метод для отрисовки яблока."""
        self.randomize_position(snake_coordinates)
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake_coordinates):
        """Метод класса Apple.

        Генерирует случайные координаты для яблока.
        Принимает список координат змейки,
        с целью не допустить генерации яблока внутри змеи.
        """
        new_position = self.get_random_position()
        if new_position in snake_coordinates:
            new_position = self.get_random_position()
        self.position = new_position

    def get_random_position(self):
        """Метод, возвращающий случайные координаты для яблока."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Метод для обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция программы."""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(snake.positions, APPLE_COLOR)
    apple.draw(snake.positions)
    while True:
        event = False
        clock.tick(SPEED)
        handle_keys(snake)
        # Тут опишите основную логику игры.
        snake.move()
        snake.draw()
        snake.update_direction()
        if apple.position == snake.get_head_position():
            snake.length += 1
            event = True
        if snake.length >= 5:
            if snake.get_head_position() in snake.positions[1:]:
                screen.fill(BOARD_BACKGROUND_COLOR)
                snake.reset()
                event = True
        if event:
            apple.draw(snake.positions)
        pg.display.update()


if __name__ == '__main__':
    main()
