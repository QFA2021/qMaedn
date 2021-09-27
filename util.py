import pyglet
from enum import Enum


class Color(Enum):
    """
    Set of 4 colors. One for each player.
    """
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    RED = "red"

DOTS_PER_Q = 10

def lin2grid(i):
    if i < 40:  # regular playing field
        quarter = i // DOTS_PER_Q
        i = i % DOTS_PER_Q
        y = max(i - 4, min(4, i))
        x = max(0, min(4, 4 - i + 4))
        return rot90(x, y, quarter)
    elif i < 56:  # houses
        i = i % 40
        quarter = i // 4
        i = i % 4  # 40 normal fields plus 4 per house
        x = 5
        y = 1 + i
        return rot90(x, y, quarter)
    elif i < 72:
        i = i % 56
        quarter = i // 4
        i = i % 4
        x = i % 2
        y = 1 - i // 2
        return rot90(x, y, quarter)
    else:
        raise ValueError("Given linear index is out of bounds, max is 71")


def grid2lin(x, y):
    quarter = 0
    if y > 5 and x < 6:
        quarter = 1
    elif y > 4 and x > 5:
        quarter = 2
    elif y < 5 and x > 4:
        quarter = 3
    elif x == 5 and y == 5:
        return None

    x, y = rot90(x, y, (4 - quarter) % 4)
    print(f"q{quarter} {x}, {y}")

    # starting points
    if x + y <= 2:
        i = 56 + x + 2 - 2 * y
        return i + 4 * quarter
    # houses
    elif x > 0 and y == 5:
        i = 40 + x - 1
        return i + 4 * ((quarter + 1) % 4)
    # regular field
    else:
        if x == 0 and y == 5:
            i = 9
        elif y == 4 and x <= 4:
            i = 8 - x
        elif x == 4:
            i = y
        else:
            return None
        return i + 10 * quarter


def rot90(x, y, times):
    x = x - 5
    y = y - 5
    for _ in range(times):
        x, y = y, -x
    return x + 5, y + 5



def get_color(x):
  RED = (255, 0, 0)
  GREEN = (0, 255, 0)
  BLUE = (0, 0, 255)
  YELLOW = (255, 255, 0)
  DEFAULT = (0, 0, 0)
  if x == 0 or (x >= 40 and x < 44) or (x >= 56 and x < 60): 
    return RED
  elif x == 10 or (x >= 44 and x < 48) or (x >= 60 and x < 64): 
    return BLUE
  elif x == 20 or (x >= 48 and x < 52) or (x >= 64 and x < 68): 
    return GREEN
  elif x == 30 or (x >= 52 and x < 56) or (x >= 68 and x < 72): 
    return YELLOW
  else:
    return DEFAULT

  #if x == 10 or (x >= 

def test_consistency():
    for i in range(0, 72):
        x, y = lin2grid(i)
        # print(f"{i}: {x}, {y}")
        i2 = grid2lin(x, y)
        print(f"({x}, {y}) i: {i}, i2: {i2}")
        assert i == i2


if __name__ == "__main__":
    # for i in range(72):
    # x, y = lin2grid(i)
    # print(f"{i}: {x},{y}")

    for y in range(2):
        for x in range(2):
            print(f"{x}, {y}: {grid2lin(x, y)}")
    test_consistency()
