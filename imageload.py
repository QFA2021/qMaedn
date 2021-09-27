import pyglet

stonepngs = {}
fieldpngs = {}

stonelist = ['blue', 'green', 'red', 'yellow', 'b_g', 'b_r', 'b_y', 'g_b',
             'g_r', 'g_y', 'r_b', 'r_g', 'r_y', 'y_b', 'y_g', 'y_r']
fieldlist = ['hadamard', 'not', 'phase_b', 'phase_l', 'phase_r', 'phase_t']


def load_stone_pngs():
    for stone in stonelist:
        path_name = "resources/pngs/" + stone + ".png"
        img = pyglet.image.load(path_name)
        stonepngs[stone] = img

def load_field_pngs():
    for field in fieldlist:
        path_name = "resources/pngs/" + field + ".png"
        img = pyglet.image.load(path_name)
        fieldpngs[field] = img

def load_pngs():
    load_stone_pngs()
    load_field_pngs()

