import pyglet
from game import *

global board, window


if __name__ == "__main__":

    window = pyglet.window.Window(width=1000, height=1000)
    pyglet.gl.glClearColor(255, 255, 255, 1.0)
    board_batch = pyglet.graphics.Batch()
    stone_batch = pyglet.graphics.Batch()

    board = Board(window)
    board.get_batch(board_batch)
    board.get_stone_batch(stone_batch)


    @window.event
    def on_draw():
        window.clear()
        board_batch.draw()
        stone_batch.draw()

    pyglet.app.run()

