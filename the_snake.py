from random import choice, randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс, являющийся родительским для классов Snake и Apple."""

    def __init__(self):
        """Функция для инициализации экземпляра класса GameObject."""
        self.position = START_POSITION
        self.body_color = None

    def draw(self):
        """Функция для отрисовки объекта. Будет переопределяться"""
        """в классах Snake и Apple."""
        pass


class Snake(GameObject):
    """Класс Snake, наследуется от класса GameObject."""

    def __init__(self,
                 length=1,
                 positions=START_POSITION,
                 direction=RIGHT,
                 next_direction=None,
                 body_color=SNAKE_COLOR,
                 last=None):
        super().__init__()
        self.length = 1
        self.positions = [positions]
        self.direction = direction
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def move(self):
        """Функция, описывающая движение змейки."""
        head = self.get_head_position()
        x_coord, y_coord = head
        x_direction, y_direction = self.direction
        new_head = ((x_coord + x_direction * GRID_SIZE) % SCREEN_WIDTH,
                    (y_coord + y_direction * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]
        if (len(self.positions) > self.length):
            self.positions.pop(-1)

    def update_direction(self):
        """Функция, обновляющая направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Функция для отрисовки змейки."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Функция, возвращающая координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Функция, сбрасывающая все параметры змейки"""
        """для перезапуска игры."""
        self.positions = [START_POSITION]
        self.length = 1
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


class Apple(GameObject):
    """Класс Snake, наследуется от класса GameObject."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = None

    def draw(self, snake_coordinates):
        """Функция для отрисовки яблока. Принимает список координат змейки,"""
        """с целью не допустить генерации яблока внутри змеи."""
        new_position = self.randomize_position()
        if new_position in snake_coordinates:
            new_position = self.randomize_position()
        self.position = new_position
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Функция, генерирующая случайные координаты для яблока."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция для обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция программы."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake(1, START_POSITION, RIGHT, None, SNAKE_COLOR, START_POSITION)
    apple.draw(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        # Тут опишите основную логику игры.
        snake.draw()
        snake.move()
        snake.update_direction()
        snake_head = snake.get_head_position()
        if apple.position == snake_head:
            apple.draw(snake.positions)
            snake.length += 1
        if snake_head in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.draw(snake.positions)
        pygame.display.update()


if __name__ == '__main__':
    main()
