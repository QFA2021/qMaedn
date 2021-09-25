from enum import Enum

import pyglet

import util


class Color(Enum):
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    RED = 4

IDX_HADAMARD = [4, 14, 24, 34]
IDX_NOT = [9, 19, 29, 39]
IDX_PHASE_1 = [36, 26, 16, 6]
IDX_PHASE_2 = [2, 12, 22, 32]
DELTA_PHASE = { 2: (1, 0), 12: (0, -1), 22: (-1, 0), 32: (0, 1) }

class Board:

    # self.fields = self.get_coordinate_system()
    # self.players = self.initialize_players()
    def __init__(self, window):
        self.shapes = []
        self.window = window
        self.gridsize = min(*window.get_size()) // 12
        self.stones = []

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

    def get_batch(self, batch):
      self.shapes = []
      background = pyglet.graphics.OrderedGroup(0)
      middleground = pyglet.graphics.OrderedGroup(1)
      foreground = pyglet.graphics.OrderedGroup(2)
      color = (0, 0, 0)
      size = self.gridsize // 2 - 4
      width = 3
      for i in range(72):
        gx, gy = util.lin2grid(i)
        px, py = gx * self.gridsize + self.gridsize//2, gy * self.gridsize + self.gridsize//2
        color = util.get_color(i)
        
        if i in IDX_HADAMARD:
          label_text = 'H'
          label_size = 36
        elif i in IDX_NOT:
          label_text = 'X'
          label_size = 36
        elif i in IDX_PHASE_1:
          pass
        else:
          label_text = str(i)
          label_size = 12

        outer_circle = pyglet.shapes.Circle(px, py, size, color=color, batch=batch, group=background)
        inner_circle = pyglet.shapes.Circle(px, py, size-width, color=(255, 255, 255), batch=batch, group=middleground)
        if i in IDX_PHASE_1:
          label = pyglet.shapes.Circle(px, py, 10, color=(0, 0, 0), batch=batch, group=foreground)
        elif i in IDX_PHASE_2:
          label = pyglet.text.Label("S", font_name='Arial', font_size=36,x=px, y=py, color=(0,0,0,255), anchor_x='center', anchor_y='center',batch=batch, group=foreground)
          dx, dy = DELTA_PHASE[i]
          from_x = px + dx * size
          from_y = py + dy * size
          to_x = px + dx * self.gridsize * 2
          to_y = py + dy * self.gridsize * 2
          connector = pyglet.shapes.Line(from_x, from_y, to_x, to_y, width=3, color=(0,0,0), batch=batch, group=foreground)
          self.shapes.append(connector)
        else:
          label = pyglet.text.Label(label_text, font_name='Arial', font_size=label_size,x=px, y=py, color=(0,0,0,255), anchor_x='center', anchor_y='center',batch=batch, group=foreground)

        self.shapes.append(outer_circle)
        self.shapes.append(inner_circle)
        self.shapes.append(label)

    # draw connections between control and phase gates

      
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
