import pyglet
from game import *
from pyglet.window import mouse
from imageload import load_pngs
from util import Color
import validation

global board, window


if __name__ == "__main__":
    # finding the size of the display to get the right scale
    display = pyglet.canvas.Display()
    screen = display.get_default_screen()
    screen_width, screen_height = screen.width, screen.height
    screen_size = min(screen_height, screen_width) - 20

    window = pyglet.window.Window(width=screen_size, height=screen_size, resizable=True)
    pyglet.gl.glClearColor(255, 255, 255, 1.0)
    board = Board(window, screen_size)
    board_batch = pyglet.graphics.Batch()
    stone_batch = pyglet.graphics.Batch()

    load_pngs()

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
            if move_valid:
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
        board_batch.draw()
        stone_batch=pyglet.graphics.Batch()
        board.update_stone_batch(stone_batch)
        stone_batch.draw()

    pyglet.app.run()

