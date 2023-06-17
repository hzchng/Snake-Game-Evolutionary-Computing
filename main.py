from kivy.app import App
from kivy.uix.widget import Widget


class SnakeGame(Widget):
    pass

class SnakeGameApp(App):
    def build(self):
        return SnakeGame()


if __name__ == '__main__':
    SnakeGameApp().run()