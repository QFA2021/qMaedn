import pyglet
from game import *
from imageload import load_pngs

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
    def on_draw():
        window.clear()
        #TODO don't redraw the board since the board batch stays the same after initialisation
        board_batch.draw()
        stone_batch.draw()

    pyglet.app.run()

