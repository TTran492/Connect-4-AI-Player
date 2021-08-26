"""
file name: evaluation.py

Author: Paul Lee, Thomas Tran

Last Modification Date: 4/25/2021

description: 
Support class for minimax agent. Helps determine the 
best move for the minimax agent.
"""
class Evaluation:

    """
    class name: __init__
    precondition: funciton is initialized
    postcondition: sets what piece the bot and opponent is
    
    description: This funciton is initialized and sets
    which piece/player the bot and the opponent is. 
    """
    def __init__(self, piece):
        self.bot_piece = piece
        if self.bot_piece == 1:
            self.opp_piece = 2
        else:
            self.opp_piece = 1

    """
    class name: evaluate_window
    precondition: function is called
    postcondition: returns the calculated score
    
    Description: 
    Given a board and window, the function gives a score depending
    on how many of the same pieces are by each other.
    """
    def evaluate_window(self, board, window):
        score = 0
        if window.count(self.bot_piece) == 4:
            score += 100
        elif window.count(self.bot_piece) == 3 and window.count(board.EMPTY) == 1:
            score += 5
        elif window.count(self.bot_piece) == 2 and window.count(board.EMPTY) == 2:
            score += 2

        if window.count(self.opp_piece) == 3 and window.count(board.EMPTY) == 1:
            score -= 4

        return score

    """
    class name: score_position
    precondition: function
    postcondition: returns the calculated score
    
    description: 
    Given the board state, the function calculates the score of the board
    and returns it to the bot. 
    """
    def score_position(self, board):
        score = 0

		## Score center column
        center_array = [int(i) for i in list(board.get_board()[:, board.COLUMN_COUNT//2])]
        center_count = center_array.count(self.bot_piece)
        score += center_count * 3

		## Score Horizontal
        for r in range(board.ROW_COUNT):
            row_array = [int(i) for i in list(board.get_board()[r,:])]
            for c in range(board.COLUMN_COUNT-3):
                window = row_array[c:c+board.WINDOW_LENGTH]
                score += self.evaluate_window(board, window)

		## Score Vertical
        for c in range(board.COLUMN_COUNT):
            col_array = [int(i) for i in list(board.get_board()[:,c])]
            for r in range(board.ROW_COUNT-3):
                window = col_array[r:r+board.WINDOW_LENGTH]
                score += self.evaluate_window(board, window)

		## Score positive sloped diagonal
        for r in range(board.ROW_COUNT-3):
            for c in range(board.COLUMN_COUNT-3):
                window = [board.get_board()[r+i][c+i] for i in range(board.WINDOW_LENGTH)]
                score += self.evaluate_window(board, window)

		## Score negative sloped diagonal
        for r in range(board.ROW_COUNT-3):
            for c in range(board.COLUMN_COUNT-3):
                window = [board.get_board()[r+3-i][c+i] for i in range(board.WINDOW_LENGTH)]
                score += self.evaluate_window(board, window)

        return score

    """
    class name: score_position
    precondition: board state
    postcondition: returns the winning_move or no more valid moves
    
    description: 
    Given the board state, finds if there is a winning move or no more moves left
    """
    def is_terminal_node(self, board):
        return board.winning_move(self.bot_piece) or board.winning_move(self.opp_piece) or len(board.get_valid_locations()) == 0
