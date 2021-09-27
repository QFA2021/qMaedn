from enum import Enum
from imageload import stonepngs, fieldpngs

import pyglet

import util
from util import Color

IDX_HADAMARD = [4, 14, 24, 34]
IDX_NOT = [9, 19, 29, 39]
IDX_PHASE_1 = [36, 26, 16, 6]
IDX_PHASE_2 = [2, 12, 22, 32]
DELTA_PHASE = {2: (1, 0), 12: (0, -1), 22: (-1, 0), 32: (0, 1)}


class Board:

    def __init__(self, window):
        """
        The Board manages the batches of the playing board and the stones.
        :param window:Window
                The pyglet window where the game is displayed
        """
        self.shapes = []
        self.window = window
        self.gridsize = min(*window.get_size()) // 12
        self.stones = self.__initialize_stones()
        self.field_map = self.init_field_map()
        self.sprites = []
        self.stone_on_the_move = None

    def init_field_map(self):
        field_map = {}
        for stone in self.stones:
            print(stone.position)
            field_map[stone.position] = stone
        return field_map

    def update_stone_batch(self, batch):
        """
        Continuously called when the application runs. Updates the visuals for everything
        that happens on the board, e.g. position and color of the stones.
        :param batch:Batch
                The pyglet batch which is used for the stones.
        :return:
        """

        for stone in self.stones:
            if stone.entangled:
                stone_name = stone.get_colours()[0].value[0] + "_" + stone.get_colours()[1].value[0]
            else:
                stone_name = stone.get_colour().value

            img = stonepngs[stone_name]
            img.anchor_x = img.height // 2
            img.anchor_y = img.height // 2

            gx, gy = util.lin2grid(stone.position)
            px, py = gx * self.gridsize + self.gridsize // 2, gy * self.gridsize + self.gridsize // 2

            sprite = pyglet.sprite.Sprite(img, px, py, batch=batch)
            sprite.scale = 0.5
            self.sprites.append(sprite)

    def __initialize_stones(self):
        """
        Called when the board is created to put the stones into their starting positions.
        :return:
                Returns a list of all the stone-objects. The starting positions and colors are
                stored int the stones.
        """
        stones = []
        range_dic = {Color.RED: range(56, 60), Color.BLUE: range(60, 64), Color.GREEN: range(64, 68),
                     Color.YELLOW: range(68, 72)}
        for color in range_dic:
            for i in range_dic[color]:
                stones.append(Stone(color, i))

        return stones

    def initialize_board_batch(self, batch):
        """
        Initializes the batch of the board. This only contains the visuals
        which are not changed during the game. The information for all visuals
        is stored in the batch which is handed as an input.
        :param batch:Batch
                The pyglet batch which is used for the board.
        :return:
        """
        self.shapes = []
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
            inner_circle = pyglet.shapes.Circle(px, py, size - width, color=(255, 255, 255), batch=batch,
                                                group=middleground)
            if i in IDX_PHASE_1:
                label = pyglet.shapes.Circle(px, py, 10, color=(0, 0, 0), batch=batch, group=foreground)
            elif i in IDX_PHASE_2:
                label = pyglet.text.Label("S", font_name='Arial', font_size=36, x=px, y=py, color=(0, 0, 0, 255),
                                          anchor_x='center', anchor_y='center', batch=batch, group=foreground)
                dx, dy = DELTA_PHASE[i]
                from_x = px + dx * size
                from_y = py + dy * size
                to_x = px + dx * self.gridsize * 2
                to_y = py + dy * self.gridsize * 2
                connector = pyglet.shapes.Line(from_x, from_y, to_x, to_y, width=3, color=(0, 0, 0), batch=batch,
                                               group=foreground)
                self.shapes.append(connector)
            else:
                label = pyglet.text.Label(label_text, font_name='Arial', font_size=label_size, x=px, y=py,
                                          color=(0, 0, 0, 255), anchor_x='center', anchor_y='center', batch=batch,
                                          group=foreground)

            self.shapes.append(outer_circle)
            self.shapes.append(inner_circle)
            self.shapes.append(label)

    def initialize_players(self):
        pass

    def is_occupied(self, i, color=None):
        if i not in self.field_map:
            return False
        elif color:
            return color in self.field_map[i].get_colours()
        else:
            return True

class Player:
    """
    colour: The colour that the player is represented by
    name: The name of the player
    """
    def __init__(self, color: Color, name):
        """

        :param color:Color
                The colour that the player is represented by
        :param name:str
                The name of the player
        """
        self.name = name
        self.color = color
        self.stones = []

    def set_stones(self, stones):
        """

        :param stones:

        :return:
        """
        self.stones = stones

    def add_stone(self, stone):
        self.stones.append(stone)

    def remove_stone(self, stone):
        self.stones.remove(stone)


class Stone:

    def __init__(self, color, position):
        """
        A playing stone which the players can move on the board.
        :param color:Color
                The color of the stone. Representing which player the stone belongs to.
        :param position:int
                The index of the field which encodes the position of the stone on the board.
        """
        self.__color__ = color
        self.entangled = False
        self.position = position
        self.other = None

    def get_colours(self):
        """
        Only used for entangled stones. Returns both colors of the entangled stone.
        """
        if self.entangled:
            return self.__color__, self.other.get_colour()
        else:
            return (self.__color__,)
        raise ValueError("The stone is not entangled and has no multiple colors.")

    def get_colour(self):
        """
        Only used for not entangled stones. Returns the color of the stone.
        """
        return self.__color__

    def entangle(self, other):
        """
        Entangles the stone itself with another stone on the board.
        :param other:Stone
                The other stone with which the entanglement takes place.
        :return:
        """
        self.other = other
        self.entangled = True
        other.entangled = True
        other.other = self

    def disentangle(self):
        """
        Only used for already entangled stones. Disentangles the stone and it's entangled partner.
        :return:
        """
        self.entangled = False
        self.other = None
        self.other.entangled = False
        self.other.other = None

    def draw(self, batch):
        pass

    def move_to(self, position):
        """
        Moves a stone from it's current position to a new position.
        :param position:int
                The index of the field where the stone is supposed to move to.
        :return:
        """
        # TODO: The validator validates here?
        self.position = position


class HadamardGate:
    def __init__(self, position):
        """
        A special playing field on the board which creates and destroys entanglement.
        :param position:int
                The index of the field where this special gate is located.
        """
        self.position = position

    @staticmethod
    def apply(self, stone1: Stone, stone2: Stone):
        """

        :param self:
        :param stone1:
        :param stone2:
        :return:
        """
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
