import pyglet
import random
import numpy as np


# create a snake class that can move around the screen using pyglet
class Snake:
    def __init__(
        self,
        x, y, init_length=3,
        head_color=(0, 255, 0),
        body_color=(255, 255, 255)
    ):
        self.positions = []
        self.direction = None
        self.head_color = head_color
        self.body_color = body_color
        self.init_length = init_length

        for i in range(init_length):
            self.positions.append((x - i, y))

    def move(self, dx, dy):
        if self.direction is not None:
            self.positions = [(self.positions[0][0] + dx, self.positions[0][1] + dy)] + self.positions[:-1]

    def grow(self, dx, dy):
        self.positions = [(self.positions[0][0] + dx, self.positions[0][1] + dy)] + self.positions

    def apple_distance_from_snake(self, apple_position):
        # to calculate distance between apple and snake.
        return np.linalg.norm(np.array(apple_position) - np.array(self.positions[0]))

