"""
File Name: board.py

Author: Paul Lee, Thomas Tran

Last Modification Date: 4/25/2021

Description:
Holds class for connect 4 board. Does the following things:
1. Holds the board state
2. Copy board
3. Get the row and column location
4. Drop a piece into desired spot
5. Check valid move
6. Print the board state
7. Check if there's a winning state
"""
import numpy as np
import copy

class Board:
    ROW_COUNT = 6           #amount of rows in connect 4 board
    COLUMN_COUNT = 7        #amount of columns in connect 4 board

    EMPTY = 0               #represents an empty space on board
    PLAYER1_PIECE = 1       #represents player 1 piece on board
    PLAYER2_PIECE = 2       #represents player 2 piece on board

    WINDOW_LENGTH = 4

    PREV_MOVE = None        #holds the previous move made
    PREV_PLAYER = None      #holds who the previous player was
    CURR_PLAYER = None      #holds who is the current player making a move

    """
    function name: __init__
    precondition: board state and current_player
    postcondition: none
    
    Description:
    Initialize the board states
    """
    def __init__(self, current_player):
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT), dtype=int)
        self.num_slots_filled = 0
        self.CURR_PLAYER = current_player
        self.PREV_PLAYER = self.get_opp_player(current_player)

    """
    function name: copy_board
    precondition: board state
    postcondition: returns a copy of the board
    
    Description: 
    Copys the board state
    """
    def copy_board(self):
        c = copy.deepcopy(self)
        return c

    """
    function name: get_board
    precondition: board
    postcondition: returns board state
    
    Description: 
    returns the board state
    """
    def get_board(self):
        return self.board

    """
    function name: get_row_col
    precondition: board, row, col
    postcondition: returns the location as specifired row and column
    
    Description:
    function to retrieve the wanted position at row and col
    """
    def get_row_col(self, row, col):
        return self.board[row][col]
    
    """
    function name: get_opp_player
    precondition: board, current player
    postcondition: returns the other player piece
    
    Description: 
    Function to help move to the next player after the current player makes a move
    """
    def get_opp_player(self, piece):
        if piece == self.PLAYER1_PIECE:
            return self.PLAYER2_PIECE
        else:
            return self.PLAYER1_PIECE

    """
    function name: drop_piece
    precondition: board, column, current player
    postcondition: move made and moves to next players
    
    Description:
    Once a player makes a move, the move is made and 
    moves to the next player
    """
    def drop_piece(self, col, piece):
        row = self.get_next_open_row(col)
        self.board[row][col] = piece
        self.num_slots_filled += 1
        self.PREV_MOVE = col
        self.PREV_PLAYER = piece
        self.CURR_PLAYER = self.get_opp_player(piece)

    """
    function name: is_valid_location
    precondition: move is made
    postcondition: returns if move is valid or not
    
    Description:
    makes sure that the move a player makes is valid
    """
    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT-1][col] == 0
        
    
    """
    function name: get_next_open_row
    precondition: none
    postcondition: returns an open row
    
    Description:
    checks to see if there is an open row
    """    
    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r


    """
    function name: print_board
    precondition: function is called
    postcondition: prints current board state
    
    Description:
    Prints the board state
    """
    def print_board(self):
        print(np.flip(self.board, 0))

    """
    function name: winning_move
    precondition: move is made
    postcondition: returns if move is a winnning position
    
    Description:
    checks if the mode that was made is a win move state
    """
    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    """
    function name: get_valid_locations
    precondition: move is made
    postcondition: returns valid locations
    
    Description:
    checks all valid column locations
    """
    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    """
    function name: check_draw
    precondition: function is called
    postcondition: returns if the drawing is filled
    
    Description:
    makes sure board is drawn correctly
    """
    def check_draw(self):
        if self.num_slots_filled == self.ROW_COUNT * self.COLUMN_COUNT:
            return True
        return False

    """
    function name: search_result
    precondition: function is called
    postcondition: searches for winning move
    
    Description:
    checks winning move
    """
    def search_result(self, piece):
        if self.winning_move(piece):
            return 1
        elif self.winning_move(self.get_opp_player(piece)):
            return 0
        elif not self.get_valid_locations():
            return 0.5
