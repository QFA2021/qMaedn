import pyglet
from enum import Enum
from pyglet import shapes

class Color(Enum):
    GREEN = 1
    BLUE = 2
    YELLOW = 3
    RED = 4


class Board:

       # self.fields = self.get_coordinate_system()
       # self.players = self.initialize_players()


    def get_coordinate_system(self):
        w_pixel_size = self.w // 11
        h_pixel_size = self.h // 11
        fields = []

        for y in range(0, 11):
            y1 = y * h_pixel_size
            y2 = y * h_pixel_size + h_pixel_size
            for x in range(0, 11):
                x1 = x * w_pixel_size
                x2 = x * w_pixel_size + w_pixel_size
                field = Field(x1, x2, y1, y2, (x+1) * (y+1))
                fields.append(field)
        return fields

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
    def __init__(self, colour, position):
        self.colour = colour
        self.entangled = False
        self.position = position
        self.other = None

    def change_colour(self, new_colour):
        self.colour = new_colour

    def is_entangled(self):
        return self.entangled

    def entangle(self, other):
        self.other = other

    def disentangle(self):
        pass

    def draw(self, canvas):
        pass



class HadamardGate:
    def __init__(self, field):
        self.field = field

    @staticmethod
    def apply(self, stone1: Stone, stone2: Stone):
        stone1.entangled = True
        stone2.entangled = True


if __name__ == "__main__":
    Board()
