import random
import time

import pyglet

import util
from imageload import stonepngs, fieldpngs, dicepngs
from util import Color
from util import get_screensize

IDX_HADAMARD = [4, 14, 24, 34]
IDX_NOT = [9, 19, 29, 39]
IDX_PHASE_1 = [36, 26, 16, 6]
IDX_PHASE_2 = [2, 32, 22, 12]
DELTA_PHASE = {2: (1, 0), 12: (0, -1), 22: (-1, 0), 32: (0, 1)}


class Board:

    def __init__(self, window):
        """
        The Board manages the batches of the playing board and the stones.
        :param window:Window
                The pyglet window where the game is displayed
        """
        self.shapes = []
        self.sprites = []
        self.diceimage = None
        self.roll_the_dice = False

        self.window = window
        self.screensize = min(get_screensize())        # takes the min of height and width of the screen
        self.gridsize = min(*window.get_size()) // 13  # 12 to cover the whole window

        self.stones = self.initialize_stones()
        self.field_map = self.init_field_map()
        self.gate_map = self.init_gate_map()

        self.current_player = None
        self.current_dicevalue = 1
        self.players = self.initialize_players()

        self.state = util.State.WAIT_DICE           #util.State.START

        self.stone_on_the_move = None
        self.stone_to_be_paired = None
        self.stone_to_be_unpaired = None

    def init_field_map(self):
        field_map = {}
        for stone in self.stones:
            #(stone.position)
            field_map[stone.position] = stone
        return field_map

    def init_gate_map(self):
        gate_map = {}
        for idx_h, idx_not in zip(IDX_HADAMARD, IDX_NOT):
            gate_map[idx_h] = HadamardGate(idx_h)
            gate_map[idx_not] = XGate(idx_not)
        for idx_1, idx_2 in zip(IDX_PHASE_1, IDX_PHASE_2):
            gate = PhaseShiftGate((idx_1, idx_2))
            gate_map[idx_1] = gate
            gate_map[idx_2] = gate
        return gate_map

    def update_stone_batch(self, batch):
        """
        Continuously called when the application runs. Updates the visuals for everything
        that happens on the board, e.g. position and color of the stones.
        :param batch:Batch
                The pyglet batch which is used for the stones.
        :return:
        """
        print(self.state)
        for stone in self.stones:
            if stone.entangled:
                stone_name = stone.get_colours()[0].value[0] + "_" + stone.get_colours()[1].value[0]
            else:
                stone_name = stone.get_colour().value

            img = stonepngs[stone_name]
            img.anchor_x = img.height // 2
            img.anchor_y = img.height // 2

            px, py = util.lin2pix(stone.position, self.gridsize)

            sprite = pyglet.sprite.Sprite(img, px, py, batch=batch)
            sprite.scale = 0.5 * self.screensize / 1000
            self.sprites.append(sprite)

        self.draw_dice(self.current_dicevalue, batch)

    def update_dice_batch(self, batch):
        i = random.randint(1,6)
        self.draw_dice(i, batch)
        self.roll_the_dice = False

    def initialize_stones(self):
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

        background = pyglet.graphics.OrderedGroup(0)
        middleground = pyglet.graphics.OrderedGroup(1)
        foreground = pyglet.graphics.OrderedGroup(2)

        # places all 72 fields on the according position on the board
        for position in range(72):
            gatename = 'standart'
            if position in IDX_HADAMARD:
                gatename = 'hadamard'
            elif position in IDX_NOT:
                gatename = 'not'
            elif position in (10, 44, 45, 46, 47, 60, 61, 62, 63):  # all blue fields
                gatename = 'bluefield'
            elif position in (20, 48, 49, 50, 51, 64, 65, 66, 67):  # all green fields
                gatename = 'greenfield'
            elif position in (30, 52, 53, 54, 55, 68, 69, 70, 71):  # all yellow fields
                gatename = 'yellowfield'
            elif position in (0, 40, 41, 42, 43, 56, 57, 58, 59):  # all red fields
                gatename = 'redfield'
            elif position in IDX_PHASE_2:
                orientation = {'2': 'l', '12': 't', '22': 'r', '32': 'b'}
                gatename = 'phase_' + orientation[str(position)]
            elif position in IDX_PHASE_1:
                gatename = 'phase_control'
            img = fieldpngs[gatename]
            img.anchor_x = img.height // 2
            img.anchor_y = img.height // 2

            px, py = util.lin2pix(position, self.gridsize)

            sprite = pyglet.sprite.Sprite(img, px, py, batch=batch, group=foreground)
            sprite.scale = 0.45 * self.screensize / 1000
            self.sprites.append(sprite)

            label = pyglet.text.Label(str(position), font_name='Arial', font_size=12, x=px, y=py,
                    color=(0, 0, 0, 255), anchor_x='center', anchor_y='center', batch=batch, group=foreground)

        # creating the connection lines between the phaseshift gates
        for i, j in zip(IDX_PHASE_1, IDX_PHASE_2):
            from_x, from_y = util.lin2pix(i, self.gridsize)
            to_x, to_y = util.lin2pix(j, self.gridsize)
            connector = pyglet.shapes.Line(from_x, from_y, to_x, to_y, width=5, color=(0, 0, 0), batch=batch,
                                           group=middleground)
            self.shapes.append(connector)

        # creating the background board
        img = fieldpngs['board']
        sprite = pyglet.sprite.Sprite(img, 0, 0, batch=batch, group=background)
        sprite.scale = 1 / 650 * self.screensize * 0.92
        self.sprites.append(sprite)

        # creating the dice
        self.draw_dice(1, batch)

        #creating the logo
        img = fieldpngs['logo']
        img.anchor_x = img.height // 2
        img.anchor_y = img.height // 2
        width, height = get_screensize()
        px = (max(width, height) - min(width, height))//2 + min(width, height)
        py = height // 3
        sprite = pyglet.sprite.Sprite(img, px, py, batch=batch, group=foreground)
        sprite.scale = height / img.height * 0.5
        self.sprites.append(sprite)


    def initialize_players(self):
        player_1 = Player(Color.BLUE, "Player 1")
        player_2 = Player(Color.GREEN, "Player 2")
        player_3 = Player(Color.YELLOW, "Player 3")
        player_4 = Player(Color.RED, "Player 4")

        player_1.next = player_2
        player_2.next = player_3
        player_3.next = player_4
        player_4.next = player_1
        self.current_player = player_1
        return [player_1, player_2, player_3, player_4]

    def draw_dice(self, dicevalue, batch):
        # creating the dice
        img = dicepngs[str(dicevalue)]
        img.anchor_x = img.height // 2
        img.anchor_y = img.height // 2

        position = util.grid2lin(4, 4)  # field in the bottom left of the dice
        px, py = util.lin2pix(position, self.gridsize)
        px += self.gridsize
        py += self.gridsize
        sprite = pyglet.sprite.Sprite(img, px, py, batch=batch, group=pyglet.graphics.OrderedGroup(3))
        sprite.scale = 0.45 * self.screensize / 1000
        self.diceimage = sprite


    def is_occupied(self, i, color=None):
        if i not in self.field_map:
            return False
        elif color:
            return color in self.field_map[i].get_colours()
        else:
            return True

    def throw_stone(self, i):
        # TODO implement throwing of entangled stones
        stone = self.field_map.pop(i)
        start, _ = util.start_coordinates[stone.get_colour()]
        new_pos = start
        while self.is_occupied(new_pos) and new_pos < start + 4:
            new_pos += 1
        print(f'moving thrown stone to {new_pos}')
        self.field_map[new_pos] = stone
        stone.move_to(new_pos)
    
    def phase_shift(self):
        print('performing phase shift operation')
        new_field_map = {}
        for i in self.field_map:
            if i >= 40:
                continue
            new_position = (i + 10) % 40
            print(f"shifting from {i} to {new_position}")
            stone = self.field_map[i]
            new_field_map[new_position] = stone
            stone.move_to(new_position)
        self.field_map = new_field_map
    
    # note: this counts the number of *HALF* stones to account for entanglement
    def count_stones_per_color(self):
        count_map = {}
        for (_, stone) in self.field_map.items():
            if not stone.entangled:
                if not stone.color in count_map:
                    count_map[stone.color] = 0
                count_map[stone.color] += 2
            else:
                color_1, color_2 = stone.get_colours()
                for color in [color_1, color_2]:
                    if not color in count_map:
                        count_map[stone.color] = 0
                    count_map[stone.color] += 1
        return count_map


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
        self.next = None


class Stone:

    def __init__(self, color, position):
        """
        A playing stone which the players can move on the board.
        :param color:Color
                The color of the stone. Representing which player the stone belongs to.
        :param position:int
                The index of the field which encodes the position of the stone on the board.
        """
        self.color = color
        self.entangled = False
        self.position = position
        self.other = None

    def get_colours(self):
        """
        Only used for entangled stones. Returns both colors of the entangled stone.
        """
        if self.entangled:
            return self.color, self.other.get_colour()
        else:
            return (self.color,)

    def get_colour(self):
        """
        Only used for not entangled stones. Returns the color of the stone.
        """
        return self.color

    def entangle(self, otherStone):
        """
        Entangles the stone itself with another stone on the board.
        :param otherStone:Stone
                The other stone with which the entanglement takes place.
        :return:
        """
        self.other = otherStone
        self.entangled = True
        otherStone.entangled = True
        otherStone.other = self

    def disentangle(self, col1, col2):
        """
        Only used for already entangled stones. Disentangles the stone and its entangled partner.
        """
        self.entangled = False
        self.other.entangled = False
        self.other.other = None
        self.color = col1
        self.other.color = col2
        self.other = None

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
        self.name = util.Gate.H
        self.position = position

    @staticmethod
    def apply(self, stone1: Stone, stone2: Stone):
        """

        :param self:
        :param stone1:
        :param stone2:
        :return:
        """
        stone1.entangle(stone2)


class XGate:
    def __init__(self, position):
        self.position = position
        self.name = util.Gate.X

    @staticmethod
    def apply(self, stone: Stone, color: Color):
        stone.color = color


class PhaseShiftGate:
    def __init__(self, position):
        assert len(position) == 2
        self.position = position
        self.name = util.Gate.S

    @staticmethod
    def apply():
        pass
