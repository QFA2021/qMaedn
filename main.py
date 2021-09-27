import pyglet
from game import *
from pyglet.window import mouse
import random

from imageload import load_pngs
from util import Color
import validation

global board, window



class Controls:
    
    def __init__(self, x, y):
        self.shapes = []
        self.x = x
        self.y = y
        self.diceval = 1

    def throw_die(self):
        self.diceval = random.randint(1,6)

    def update_batch(self, batch):
        label_text = f'Dice roll: {self.diceval}'
        label = pyglet.text.Label(label_text, font_name='Arial', font_size=36, x=self.x, y=self.y,
                                          color=(0, 0, 0, 255), anchor_x='center', anchor_y='center', batch=batch)
        self.shapes.append(label)


if __name__ == "__main__":

    window = pyglet.window.Window(width=1000, height=1000)
    pyglet.gl.glClearColor(255, 255, 255, 1.0)
    board_batch = pyglet.graphics.Batch()
    stone_batch = pyglet.graphics.Batch()
    control_batch = pyglet.graphics.Batch()

    load_pngs()

    board = Board(window)
    board.initialize_board_batch(board_batch)
    board.update_stone_batch(stone_batch)
    
    controls = Controls(window.width//2, 950)


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        position = util.pix2lin(x,y, board.gridsize)
        print(position)
        if position in board.field_map:
            stone = board.field_map[position]
            board.stone_on_the_move = stone


    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if board.stone_on_the_move is not None:
            stone = board.stone_on_the_move
            new_position = util.pix2lin(x, y, board.gridsize)
            print(new_position)
            move_valid = validation.validate(stone.position, new_position, 6, stone.get_colour(), board)
            print(move_valid)
            if move_valid:
                board.field_map.pop(stone.position)
                board.field_map[new_position] = stone
                stone.move_to(new_position)
                board.stone_on_the_move = None

    @window.event
    def on_draw():
        window.clear()
        #TODO don't redraw the board since the board batch stays the same after initialisation
        board_batch.draw()
        stone_batch=pyglet.graphics.Batch()
        board.update_stone_batch(stone_batch)
        stone_batch.draw()
        controls.update_batch(control_batch)
        control_batch.draw()

    pyglet.app.run()



