import pyglet

"""
These 2 dictionaries contain all pngs. They are imported to game.py. Therefore the pngs are
only loaded once at the beginning in the main file.
"""
stonepngs = {}                  # keys: stonenames e.g. 'g_r'           values: loaded pngs
fieldpngs = {}                  # keys: fieldnames e.g. 'hadamard'      values: loaded pngs
dicepngs = {}                   # keys: '1' to '6'                      values: loaded pngs
textpngs = {}


# filenames needed to construct the paths
stonelist = ['blue', 'green', 'red', 'yellow', 'b_g', 'b_r', 'b_y', 'g_b',
             'g_r', 'g_y', 'r_b', 'r_g', 'r_y', 'y_b', 'y_g', 'y_r']
fieldlist = ['hadamard', 'not', 'phase_b', 'phase_l', 'phase_r', 'phase_t', 'phase_control',
             'standart', 'bluefield', 'greenfield', 'redfield', 'yellowfield', 'board', 'logo']
textlist = ['blue_turn', 'red_turn', 'green_turn', 'yellow_turn',
            'do_dice', 'do_entangle', 'do_collapse', 'do_move']



def load_stone_pngs():
    """
    Loading all pngs of the stones and storing them in the stonepngs dictionary.
    :return:
    """
    for stone in stonelist:
        path_name = "resources/pngs/" + stone + ".png"
        img = pyglet.image.load(path_name)
        stonepngs[stone] = img

def load_field_pngs():
    """
    Loading all pngs of the fields and storing them in the fieldpngs dictionary.
    :return:
    """
    for field in fieldlist:
        path_name = "resources/pngs/" + field + ".png"
        img = pyglet.image.load(path_name)
        fieldpngs[field] = img

def load_dice_pngs():
    """
    Loading all pngs of the dice sides and storing them in the dicepngs dictionary.
    :return:
    """
    for i in range(1, 7):
        img = pyglet.image.load("resources/pngs/" + str(i) + '.png')
        dicepngs[str(i)] = img

def load_text_pngs():
    for name in textlist:
        path_name = "resources/pngs/" + name + ".png"
        img = pyglet.image.load(path_name)
        textpngs[name] = img


def load_pngs():
    """
    Loading all pngs by calling each loading function.
    :return:
    """
    load_stone_pngs()
    load_field_pngs()
    load_dice_pngs()
    load_text_pngs()


