"""
file name: connect4.py

Author: Paul Lee, Thomas Tran

Last Modification Date: 4/25/2021

description:
Functions the connect4 game. Proveides the following functions:
1. next_turn
2. check_win
3. connect4
"""
import numpy as np
import os
import pygame
import sys
import math
import random
import time
from board import *
from bots import *

#pygame version number and welcome message hidden.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

board = None
gb = None

# dev statement to turn of the UI when having a bot vs bot match
# turning UI off in this case helps improve the performance of the bots.
graphics = True

PLAYER_COLOUR = [GBoard.RED, GBoard.YELLOW]                         #colors for player pieces

game_over = False                                                   #keeps the game running til win state
turn = random.randint(Board.PLAYER1_PIECE, Board.PLAYER2_PIECE)     #deciding whose turn it is

"""
function name: next_turn
precondition: none
postcondition: the next player to play is decided

description: 
Prints the board state, waits for the current player to make move,
then changes turn to next player
"""
def next_turn():
	global turn
	print("\nPlayer " + str(turn) + "'s Turn\n")
	board.print_board()
	if graphics:
		gb.draw_gboard(board)

	if turn == board.PLAYER1_PIECE:
		turn = board.PLAYER2_PIECE
	else:
		turn = board.PLAYER1_PIECE


"""
function name: check_win
precondition: move is made
postcondition: win state, draw state, or continue the game

description: 
Checking if the board state is a win or draw state. If so, the game 
will end.
"""
def check_win(piece):
	if board.winning_move(piece):
		if graphics:
			gb.write_on_board("PLAYER " + str(piece) + " WINS!", PLAYER_COLOUR[piece - 1], 350, 50, 70, True)
			gb.update_gboard()
		print("\nPLAYER " + str(piece) + " WINS!")
		return True
	
	if board.check_draw():
		if graphics:
			gb.write_on_board("IT'S A TIE!", gb.LIGHTBLUE, 350, 50, 70, True)
			gb.update_gboard()
		print("\n IT'S A TIE!")
		return True
	return False

"""
function name: connect4
precondition: function is called
postcondition: the connect 4 game will begin

description: 
The board ui will be shown and the game will commence.
Manages moves, time taken, and game state.
"""
def connect4(p1, p2, ui=True):
	global game_over, board, gb, graphics

	graphics=ui

	board = Board(turn)
	board.print_board()

	if graphics:
		gb = GBoard(board)
		gb.draw_gboard(board)
		gb.update_gboard()

	time_p1 = time_p2 = 0
	moves_count_p1 = moves_count_p2 = 0

	while not game_over:
		# Player1's Input
		start = time.perf_counter()
		if turn == board.PLAYER1_PIECE and not game_over:
			col = p1.get_move(board)

			if board.is_valid_location(col):
				board.drop_piece(col, board.PLAYER1_PIECE)
				moves_count_p1 += 1
				next_turn()
				game_over = check_win(board.PLAYER1_PIECE)
		end = time.perf_counter()

		time_p1 += (end - start)

		# Player2's Input
		start = time.perf_counter()
		if turn == board.PLAYER2_PIECE and not game_over:
			col = p2.get_move(board)

			if board.is_valid_location(col):
				board.drop_piece(col, board.PLAYER2_PIECE)
				moves_count_p2 += 1
				next_turn()
				game_over = check_win(board.PLAYER2_PIECE)
		end = time.perf_counter()

		time_p2 += (end - start)

		if game_over:
			pygame.time.wait(1000)

			print("\nPlayer 1")
			print("TIME: " + "{:.2f}".format(round(time_p1, 2)) + " seconds")
			print("MOVES: "+ str(moves_count_p1))
			print("\nPlayer 2")
			print("TIME: " + "{:.2f}".format(round(time_p2, 2)) + " seconds")
			print("MOVES: "+ str(moves_count_p2))

			sys.exit()

if __name__ == "__main__":
	print()
	print("use the file 'game.py' to start the game!")
