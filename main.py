import pyglet
from game import *

global board, window


if __name__ == "__main__":

    window = pyglet.window.Window(width=1000, height=1000)
    pyglet.gl.glClearColor(255, 255, 255, 1.0)
    batch = pyglet.graphics.Batch()
    board = Board(window)
    board.get_batch(batch)


    @window.event
    def on_draw():
        window.clear()
        batch.draw()

    pyglet.app.run()

