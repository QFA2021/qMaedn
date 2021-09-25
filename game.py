from enum import Enum

import pyglet

import util


class Color(Enum):
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    RED = 4


class Board:

    # self.fields = self.get_coordinate_system()
    # self.players = self.initialize_players()
    def __init__(self, window):
        self.shapes = []
        self.window = window
        self.gridsize = min(*window.get_size()) // 12
        self.stones = []
        print(self.gridsize)

    def get_batch(self, batch):
        background = pyglet.graphics.OrderedGroup(0)
        middleground = pyglet.graphics.OrderedGroup(1)
        foreground = pyglet.graphics.OrderedGroup(2)
        color = (0, 0, 0)
        size = self.gridsize // 2 - 4
        width = 3
        for i in range(72):
            gx, gy = util.lin2grid(i)
            px, py = gx * self.gridsize + self.gridsize // 2, gy * self.gridsize + self.gridsize // 2
            color = util.get_color(i)
            outer_circle = pyglet.shapes.Circle(px + size // 2, py + size // 2, size, color=color, batch=batch,
                                                group=background)
            inner_circle = pyglet.shapes.Circle(px + size // 2, py + size // 2, size - width, color=(255, 255, 255),
                                                batch=batch, group=middleground)
            text = pyglet.text.Label(str(i), font_name='Arial', font_size=12, x=px + size // 2, y=py + size // 2,
                                     color=(0, 0, 0, 255), anchor_x='center', anchor_y='center', batch=batch,
                                     group=foreground)

            self.shapes.append(outer_circle)
            self.shapes.append(inner_circle)
            self.shapes.append(text)

    def get_stone_batch(self, batch):
        range_dic = {Color.RED: range(56, 60), Color.BLUE: range(60, 64), Color.GREEN: range(64, 68),
                     Color.YELLOW: range(68, 72)}
        size = self.gridsize // 2 - 4
        width = 3

        for color in range_dic:
            for i in range_dic[color]:
                self.stones.append(Stone(color, i))
                gx, gy = util.lin2grid(i)
                px, py = gx * self.gridsize + self.gridsize // 2, gy * self.gridsize + self.gridsize // 2

                circle = pyglet.shapes.Circle(px + size // 2, py + size // 2, size - width, color=util.get_color(i),
                                              batch=batch)
                self.shapes.append(circle)

    def initialize_players(self):
        pass


class Player:
    """
    colour: The colour that the player is represented by
    name: The name of the player
    """

    def __init__(self, color: Color, name):
        self.name = name
        self.color = color
        self.stones = []

    def set_stones(self, stones):
        self.stones = stones

    def add_stone(self, stone):
        self.stones.append(stone)

    def remove_stone(self, stone):
        self.stones.remove(stone)


class Stone:
    def __init__(self, color, position):
        self.__color__ = color
        self.entangled = False
        self.position = position
        self.other = None

    def get_colour(self):
        if self.entangled:
            return self.__color__, self.other.__color__
        return self.__color__, None

    def entangle(self, other):
        self.other = other
        self.entangled = True

    def disentangle(self):
        self.entangled = False
        self.other = None
        # TODO: Change color or position?

    def draw(self, batch):
        pass

    def move_to(self, position):
        # TODO: The validator validates here?
        self.position = position


class HadamardGate:
    def __init__(self, position):
        self.position = position

    @staticmethod
    def apply(self, stone1: Stone, stone2: Stone):
        stone1.entangled = True
        stone2.entangled = True


class XGate:
    def __init__(self, position):
        self.position = position

    @staticmethod
    def apply(self, stone: Stone, color: Color):
        stone.color = color


class PhaseShiftGate:
    def __init__(self, position):
        self.position = position

    @staticmethod
    def apply():
        pass
