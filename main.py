import pyglet
from game import *
from pyglet.window import mouse
from imageload import load_pngs
from util import Color
import validation

global board, window


if __name__ == "__main__":

    window = pyglet.window.Window(width=1000, height=1000)
    pyglet.gl.glClearColor(255, 255, 255, 1.0)
    board_batch = pyglet.graphics.Batch()
    stone_batch = pyglet.graphics.Batch()

    load_pngs()

    board = Board(window)
    board.initialize_board_batch(board_batch)
    board.update_stone_batch(stone_batch)


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
            if not new_position:
                return
            print(new_position)
            move_valid = validation.validate(stone.position, new_position, 6, stone.get_colour(), board)
            print(move_valid)
            if move_valid or not move_valid:
                if board.is_occupied(new_position):
                    print(f'throwing stone at {new_position}')
                    board.throw_stone(new_position)
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

    pyglet.app.run()

