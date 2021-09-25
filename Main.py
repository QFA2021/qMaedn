import pyglet
from Game import *

global board, window




if __name__ == "__main__":

    board = Board()
    window = pyglet.window.Window(width=500, height=500)
    batch = pyglet.graphics.Batch()
  #  board.get_batch(batch)
    circle = pyglet.shapes.Circle(100,100,50, color=(255,255,0), batch=batch)


    @window.event
    def on_draw():
        window.clear()

        batch.draw()

    pyglet.app.run()

