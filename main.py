import pyglet
from game import *
from pyglet.window import mouse
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
    def on_mouse_press(x, y, button, modifiers):
        pass


    @window.event
    def on_mouse_release(x, y, button, modifiers):
        pass

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            gridsize = min(*window.get_size()) // 12
            position = util.grid2lin(x//gridsize, y//gridsize)
            print(position)
            if position in board.field_map:
                print("found")
                stone = board.field_map[position]
                new_x = x + dx
                new_y = y + dy
                new_position = util.grid2lin(new_x, new_y)
                stone.move_to(new_position)
                board.field_map.pop(position)
                board.field_map[new_position] = stone

    @window.event
    def on_draw():
        window.clear()
        #TODO don't redraw the board since the board batch stays the same after initialisation
        board_batch.draw()
        stone_batch.draw()

    pyglet.app.run()


