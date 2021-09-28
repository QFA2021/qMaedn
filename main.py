import validation
from game import *
from imageload import load_pngs
from util import State, get_screensize, Gate

global board, window

if __name__ == "__main__":
    screen_size = get_screensize()
    window = pyglet.window.Window(width=screen_size, height=screen_size, resizable=True)
    pyglet.gl.glClearColor(255, 255, 255, 1.0)
    board = Board(window)
    board_batch = pyglet.graphics.Batch()
    stone_batch = pyglet.graphics.Batch()

    load_pngs()

    board.initialize_board_batch(board_batch)
    board.update_stone_batch(stone_batch)


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        position = util.pix2lin(x, y, board.gridsize)
        if position is None:
            return
        if board.state == State.WAIT_PAIR:
            # if the selected position corresponds to a stone and the stone has
            # a different color and the stone is not already entangled, then entangle
            if position in board.field_map and (not board.field_map[position].entangled) and board.field_map[
                position].get_colour() is not board.current_player:
                board.field_map[position].entangle(board.stone_to_be_paired)
                board.state = State.WAIT_DICE
                board.current_player = board.current_player.next

        elif board.state == State.WAIT_COLLAPSE:
            if position in board.field_map:

                # TODO: current player is no longer a color
                # TODO: fix different colors problem
                if board.field_map[position] == board.stone_to_be_unpaired.other or board.field_map[position] == board.stone_to_be_unpaired:
                    c1, c2 = board.field_map[position].get_colours()
                    if c1 == board.current_player.color:
                        other_color = c2
                    else:
                        other_color = c1
                    board.field_map[position].disentangle(board.current_player.color, other_color)
                    board.state = State.WAIT_DICE
                    board.stone_to_be_unpaired = None
                    board.current_player = board.current_player.next


        elif position in board.field_map:
            stone = board.field_map[position]
            board.stone_on_the_move = stone


    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if board.stone_on_the_move is not None:
            stone = board.stone_on_the_move
            new_position = util.pix2lin(x, y, board.gridsize)
            if not new_position:
                return
            print(new_position, board.state)
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
                board.current_player = board.current_player.next


            if new_position in board.gate_map:
                if board.gate_map[new_position].name == Gate.H:
                    if stone.entangled:
                        board.state = State.WAIT_COLLAPSE
                        board.stone_to_be_unpaired = stone
                    else:
                        board.state = State.WAIT_PAIR
                        board.stone_to_be_paired = stone


                elif board.gate_map[new_position].name == Gate.X:
                    board.stone_to_be_paired = stone
                    board.state = State.WAIT_COLOR
                    board.field_map[new_position].color = Color.RED
                elif board.gate_map[new_position].name == Gate.S:
                    idx_1, idx_2 =  board.gate_map[new_position].position
                    if board.is_occupied(idx_1) and board.is_occupied(idx_2):
                        board.phase_shift()
                    board.state = State.START

    @window.event
    def on_draw():
        window.clear()
        board_batch.draw()
        stone_batch = pyglet.graphics.Batch()
        board.update_stone_batch(stone_batch)
        stone_batch.draw()


    pyglet.app.run()
