from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivy.core.window import Window
import random

BORDER = 30
SIZE = 10
Window.size = (450, 600)

ARROW = {
    'up': 82,
    'down': 81,
    'left': 80,
    'right': 79
}


LabelBase.register(
    name='Arcade',
    fn_regular='assets/prolamina_2_update.ttf'
)


class Apple(Widget):
    pass


class SnakeHead(Widget):
    pass


class SnakeBody(Widget):
    pass


class Snake(Widget):
    def __init__(self, pos, init_length=3, **kwargs):
        super().__init__(**kwargs)
        self.init_length = init_length
        self.pos = pos
        self.orient = (SIZE, 0)  # right

        while len(self.children) != init_length:
            self.spawn_snake()

    def spawn_snake(self):

        if len(self.children) == 0:
            body = SnakeHead()
            body.pos = self.pos
            self.add_widget(body)

        else:
            self.add_body()

    def add_body(self):
        body = SnakeBody()
        last_part = self.children[0]
        body.pos = last_part.x - self.orient[0], last_part.y - self.orient[1]
        body.size = last_part.size
        self.add_widget(body)

    def is_direction_blocked(self):
        snake_head = self.children[-1]
        next_step = snake_head.copy()
        next_step = next_step.x + self.orient[0], next_step.y + self.orient[1]
        if self.collision_with_boundaries(next_step) \
                or self.collision_with_self(next_step):
            return True
        return False

    # Function to check if snake has collided with a boundary.
    def collision_with_boundaries(self, snake_start=None):
        if snake_start is None:
            snake_start = self.children[-1]

        if (
                snake_start.x >= self.parent.width - BORDER
                or snake_start.y >= self.parent.height - BORDER
                or snake_start.x < BORDER
                or snake_start.y < BORDER
            ):
            return True
        return False

        # if snake_start[0] >=  or snake_start[0] < 0 or snake_start[1] >= 500 or snake_start[1] < 0:
        #     return 1
        # return False

    # Function to check if snake has collided with itself.
    def collision_with_self(self, snake_start=None):
        if snake_start is None:
            snake_start = self.children[-1]

        snake_position = [x.pos for x in self.children[:-1]]
        if snake_start.pos in snake_position:
            return True
        return False

    # Function to check if snake has reached apple.
    def collision_with_apple(self, gp):
        head_pos = self.children[-1].pos
        for apple in gp.apples:
            if apple.collide_point(*head_pos):
                gp.remove_widget(apple)
                gp.apples.remove(apple)
                self.add_body()
                return True
        return False

    def move(self):
        dx, dy = self.orient
        children = self.children
        for index, body_part in enumerate(children):
            body_part.pre_pos = body_part.pos.copy()
            if index == (len(children) - 1):  # first body part
                new_x = body_part.x + dx
                new_y = body_part.y + dy
                body_part.pos = (new_x, new_y)
            else:
                body_part.pos = children[index + 1].pos


class GamePanel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apples = []
        self.snake = None

    def init_apple(self):
        apple = Apple()
        pos = self.random_pos()
        while True:
            child_pos_collide_apple = [
                child.collide_point(*pos) for child in self.snake.children
            ]
            if any(child_pos_collide_apple):
                pos = self.random_pos()
            else:
                break

        apple.pos = pos
        self.add_widget(apple)
        return apple

    def spawn_apple(self, num_apples=5):
        while len(self.apples) != num_apples:
            self.apples.append(self.init_apple())

    def random_pos(self):
        return (
            random.randint(3, int(self.size[0] / SIZE) - 3) * SIZE,
            random.randint(3, int(self.size[1] / SIZE) - 3) * SIZE
        )

    def init_snake(self):
        if self.snake is None:
            pos = (
                int(self.width / 2 / SIZE) * SIZE,
                int(self.height / 2 / SIZE) * SIZE
            )
            self.snake = Snake(pos=pos, init_length=3)
            self.add_widget(self.snake)


class SnakeGame(Widget):
    def __init__(self, fps, **kwargs):
        super().__init__(**kwargs)
        # 0 is panel, 1 is score
        self.game_panel = self.children[0].children[0]
        self.score_board = self.children[0].children[1]
        Window.bind(on_key_down=self.key_action)
        self.clock = Clock.schedule_interval(self.update, fps)

    def update(self, dt):
        gp = self.game_panel
        gp.init_snake()
        gp.spawn_apple()

        snake = gp.snake

        # move snake
        snake.move()

        if snake.collision_with_apple(gp):
            self.score_board.value += 1

        end_cond_1 = snake.collision_with_self()
        end_cond_2 = snake.collision_with_boundaries()

        if any([end_cond_1, end_cond_2]):
            self.game_over()

    def game_over(self):
        self.clock.cancel()
        print(f"Final Value: {self.score_board.value}")
        exit()

    def key_action(self, *args):
        """This handles user input
        """
        snake = self.game_panel.snake
        up_orient = (0, SIZE)
        down_orient = (0, -SIZE)
        left_orient = (-SIZE, 0)
        right_orient = (SIZE, 0)

        ascii_code, command = list(args)[2:4]
        if ascii_code == ARROW['up'] and snake.orient != down_orient:
            snake.orient = up_orient
        elif ascii_code == ARROW['down'] and snake.orient != up_orient:
            snake.orient = down_orient
        elif ascii_code == ARROW['left'] and snake.orient != right_orient:
            snake.orient = left_orient
        elif ascii_code == ARROW['right'] and snake.orient != left_orient:
            snake.orient = right_orient


class SnakeApp(App):
    def build(self):
        game = SnakeGame(size=Window.size, fps=self.FRAME_PER_SECOND)
        return game

    def set_frame_per_second(self, frame=60):
        self.FRAME_PER_SECOND = 1.0 / frame # 60 fps


if __name__ == '__main__':
    app = SnakeApp()
    app.set_frame_per_second(10)
    app.run()