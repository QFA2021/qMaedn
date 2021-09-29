import pyglet.graphics
import time

import validation
from game import *
from pyglet.window import mouse
import random

from imageload import load_pngs
from util import State, get_screensize, Gate

global board, window


if __name__ == "__main__":
    width, height = get_screensize()
    window = pyglet.window.Window(width=width, height=height, resizable=True)
    pyglet.gl.glClearColor(255, 255, 255, 1.0)
    board = Board(window)

    board_batch = pyglet.graphics.Batch()
    stone_batch = pyglet.graphics.Batch()
    dice_batch = pyglet.graphics.Batch()
    gamelog_batch = pyglet.graphics.Batch()

    load_pngs()

    board.initialize_board_batch(board_batch)
    board.initialize_gamelog_batch(gamelog_batch)
    board.update_stone_batch(stone_batch)


    @window.event
    def on_mouse_press(x, y, button, modifiers):
        position = util.pix2lin(x, y, board.gridsize)
        print(f'position: {position}')

        if board.state == State.WAIT_DICE:
            if position == 'dice':
                board.current_dicevalue = random.randint(1,6)
                board.roll_the_dice = True
                print(f'you diced a {board.current_dicevalue}')
                board.state = State.WAIT_MOVE
            else:
                return

        elif position is None or position == 'dice':
            return
        if board.state == State.WAIT_PAIR:
            # if the selected position corresponds to a stone and the stone has
            # a different color and the stone is not already entangled, then entangle
            if position in board.field_map and (not board.field_map[position].entangled) and board.field_map[
                position].get_colour() is not board.current_player.color:
                board.field_map[position].entangle(board.stone_to_be_paired)
                board.state = State.WAIT_DICE
                board.current_player = board.current_player.next
                print(board.current_player.name)

        elif board.state == State.WAIT_COLLAPSE:
            if position in board.field_map:
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
                    print(board.current_player.name)


        elif position in board.field_map and board.state == State.WAIT_MOVE:
            stone = board.field_map[position]
            if board.current_player.color not in stone.get_colours():
                return
            else:
                board.stone_on_the_move = stone


    @window.event
    def on_mouse_release(x, y, button, modifiers):
        if board.stone_on_the_move is not None:
            stone = board.stone_on_the_move
            print("x: ", x, "y: ", y)
            new_position = util.pix2lin(x, y, board.gridsize)
            if new_position is None or new_position == 'dice':
                return
            print("New position: ", new_position)
            move_valid = validation.validate(stone.position, new_position, board.current_dicevalue, stone.get_colour(), board)
            print(move_valid)
            if move_valid:
                if board.is_occupied(new_position):
                    print(f'throwing stone at {new_position}')
                    board.throw_stone(new_position)
                board.field_map.pop(stone.position)
                board.field_map[new_position] = stone
                stone.move_to(new_position)
                board.stone_on_the_move = None


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
                else:
                    board.state = State.WAIT_DICE
                    if board.current_dicevalue != 6:
                        board.current_player = board.current_player.next
                    print(board.current_player.name)


    @window.event
    def on_draw():
        window.clear()
        board_batch.draw()
        board.update_gamelog_batch(gamelog_batch)
        gamelog_batch.draw()
        stone_batch = pyglet.graphics.Batch()
        board.update_stone_batch(stone_batch)
        stone_batch.draw()

        if board.roll_the_dice:
            board.update_dice_batch(dice_batch)
            dice_batch.draw()


    pyglet.app.run()