import pyglet
from enum import Enum
from pyglet import shapes

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
      self.gridsize = min(*window.get_size()) // 11


    def get_batch(self, batch):
      size = self.gridsize // 2 - 10
      self.shapes.append(pyglet.shapes.Circle(self.gridsize // 2,self.gridsize //2, self.gridsize // 2, color=(255,255,0), batch=batch))
      for i in range(72):
        pass
      

    def initialize_players(self):
        player_1 = Player(Color.GREEN, "P1")
        player_1.set_stones(Stone(Color.GREEN, 1))
        player_1.set_stones(Stone(Color.GREEN, 2))
        player_1.set_stones(Stone(Color.GREEN, 12))
        player_1.set_stones(Stone(Color.GREEN, 13))


        player_2 = Player(Color.BLUE, "P2")
        player_3 = Player(Color.YELLOW, "P3")
        player_4 = Player(Color.RED, "P4")




class Player:
    """
    colour: The colour that the player is represented by
    name: The name of the player
    """

    def __init__(self, color:Color, name):
        self.name = name
        self.color = color
        self.stones = []

    def set_stones(self, stones):
        self.stones = stones

    def add_stone(self, stone):
        self.stones.append(stone)

    def remove_stone(self, stone):
        self.stones.remove(stone)


class Field:
    def __init__(self, x1, x2, y1, y2, id):
        self.id = id

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


class Stone:
    def __init__(self, color, position):
        self.color = color
        self.entangled = False
        self.position = position
        self.other = None

    def set_colour(self, color):
        self.color = color

    def is_entangled(self):
        return self.entangled

    def entangle(self, other):
        self.other = other

    def disentangle(self):
        self.entangled = False
        self.other = None
        #TODO: Change color or position?

    def draw(self, batch):
        pass

    def move_to(self, position):
        #TODO: The validator validates here?
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
    def apply(self, stone: Stone, color:Color):
        stone.color = color

class PhaseShiftGate:
    def __init__(self, position):
        self.position = position

    @staticmethod
    def apply():
        pass