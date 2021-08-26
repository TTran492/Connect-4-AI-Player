"""
file name: graphics.py

Author: Paul Lee, Thomas Tran

Last Modification Date: 4/25/2021

description:
Provides the graphics for the connect 4 UI
"""
import pygame
import pygame.gfxdraw

pygame.init()

class GBoard:
    #wanted colors for graphics
    BLUE = (63,124,230)
    BLACK = (0,0,0)
    RED = (255,0,0)
    YELLOW = (255,255,0)
    WHITE = (255, 255, 255)
    LIGHTBLUE = (93, 173, 226)

    SQUARESIZE = 100

    RADIUS = int(SQUARESIZE/2 - 5)

    myfont = pygame.font.SysFont("monospace", 75)
    
    
    """
    function name: __init__
    precondition: none
    postcondition: screen will initialize with correct sizes
    
    description: 
    function to start the screen in a specific size
    """
    def __init__(self, board):
        self.width = board.COLUMN_COUNT * self.SQUARESIZE
        self.height = (board.ROW_COUNT+1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)

    """
    function name: update_gboard
    precondition: none
    postcondition: screen will update to a new state
    
    description: 
    When an event happens, this function will update the screen
    """
    def update_gboard(self):
        pygame.display.update()
    
    
    """
    function name: draw_gboard
    precondition: none
    postcondition: draws the connect 4 board
    
    description: 
    function to draw and update the connect 4 board
    """
    def draw_gboard(self, board):
        for c in range(board.COLUMN_COUNT):
            for r in range(board.ROW_COUNT):
                pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, \
                    self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), \
                    int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        
        for c in range(board.COLUMN_COUNT):
            for r in range(board.ROW_COUNT):		
                if board.get_row_col(r, c) == 1:
                    pygame.draw.circle(self.screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2),\
                         self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board.get_row_col(r, c) == 2: 
                    pygame.draw.circle(self.screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), \
                        self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        self.update_gboard()

    """
    function name: draw_rect
    precondition: none
    postcondition: draws a rectangle
    
    description: 
    given a set of parameters, the function will draw a rectangle
    """
    def draw_rect(self, colour, params):
        pygame.draw.rect(self.screen, colour, params)

    """
    function name: draw_circle
    precondition: none
    postcondition: draws a circle
    
    description: 
    given a set of parameters, the function will draw a circle
    """
    def draw_circle(self, colour, params, radius):
        pygame.draw.circle(self.screen, colour, params, radius)

    """
    function name: write_on_board
    precondition: none
    postcondition: writes wanted text
    
    description: 
    given a set of parameters, the function will write inputted text
    """
    def write_on_board(self, text, color, posx, posy, fontsize, inCenter = False):
        textfont = pygame.font.SysFont("inkfree", fontsize)
        text_surface = textfont.render(text, True, color)
        if(inCenter):
            text_position = text_surface.get_rect(center = (posx, posy))
        else:
            text_position = text_surface.get_rect(topleft = (posx, posy))
        self.screen.blit(text_surface, text_position)
    
    """
    function name: draw_button
    precondition: none
    postcondition: draws button on UI
    
    description: 
    given a set of parameters, the function will draw a button
    """
    def draw_button(self, button, screen):
        pygame.draw.rect(screen, button['color'], button['button position'], 1)
        screen.blit(button['text surface'], button['text rectangle'])

    """
    function name: create_button
    precondition: none
    postcondition: creates a button
    
    description: 
    given a set of parameters, the function will create a button
    """
    def create_button(self, posx, posy, width, height, label, callback, optional_arguments = None):
        textfont = pygame.font.SysFont("inkfree", 25)
        text_surface = textfont.render(label, True, self.WHITE)

        button_position = pygame.Rect(posx, posy, width, height)
        text_rectangle = text_surface.get_rect(topleft = (posx + 10, posy + 5))
        button = {
            'button position': button_position,
            'text surface': text_surface,
            'text rectangle': text_rectangle,
            'color': self.WHITE,
            'callback': callback,
            'args': optional_arguments,
            }
        return button