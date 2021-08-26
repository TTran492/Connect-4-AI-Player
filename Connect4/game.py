"""
File Name: game.py 

Author: Paul Lee, Thomas Tran

Last Modification Date: 4/25/2021

Description: 
The main driver to run the connect 4 game. Takes in any valid arguments
from the user and generates the game with those opeions. If there are no
arguments the driver will go to the default UI state. Depending on what
the user chooses in the UI, the driver will move to the desired state.
"""
import argparse
import sys

#pygame version number and welcome message hidden.
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from bots import *
from board import *
from connect4 import connect4


"""
bot_map dictionary
"""
bot_map = {
    'human': Human,
    'random': RandomBot,
    'minimax': MiniMaxBot,
    'montecarlo': MonteCarloBot
}

"""
name_map dictionary
"""
name_map = {
    'human': 'Human',
    'random': 'Random Bot',
    'minimax': 'MiniMax Bot',
    'montecarlo': 'Monte Carlo Tree Search Bot'
}

board = Board(1)                                                                                                                        #initialize a board

"""
Function Name: str2bool
Precondition: string
Poscondition: Returns bool condition

Description:
Converts a string to a boolean value. 
"""
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


#main function
def main(first_player = None, second_player = None):
    parser = argparse.ArgumentParser()                                                                                                  #Parser to take in pre-processor arguments
    parser.add_argument('--p1', help='Player 1 type (default Human)', type=str)                                                         #Argument to have P1 be a human
    parser.add_argument('--p2', help='Player 2 type (default Human)', type=str)                                                         #Argument to have P2 be a human
    parser.add_argument('--ui', help='turn UI off in case of a bot vs bot match', type=str2bool, nargs='?', const=True, default=True)   #Arugment to not show the UI
    parser.add_argument('--bots', help='Lists the Bots available to play with', type=str2bool, nargs='?', const=True, default=False)    #Arugment to show bots
    args = parser.parse_args()

    if args.p1 is None and args.p2 is None and args.ui and first_player is None:                                                        #If no arguments provided, go to the UI main screen
        main_screen()

    print("\n")
    if args.bots:                                                                                                                       #Shows bots, if argument is true
        print('The available bots to play with are:')
        print('Random Int Bot (random)')
        print('MiniMax Bot (minimax)')
        print('Monte Carlo Tree Search Bot (montecarlo)')
        print()
        print('Use the string in the brackets to pass as argument to p1 and p2')
        exit(1)

    p1 = p2 = None                                                                                                                      #Sets players to none
    
    if first_player != None:                                                                                                            #Sets the players
        args.p1 = first_player
        args.p2 = second_player

    if args.p1 is None or args.p2 is None:                                                                                              #In the case the previous if statement fails, exit
        print('Set both p1 and p2 args')
        sys.exit()

    if args.p1 is None or args.p1 == "human":                       #Checks if human is player 1                                                                                           
        print("Player 1 is set as a Human")
        p1 = Human(Board.PLAYER1_PIECE)                             #Set human as player 1
    else:                                                           #If not the case
        for bot in bot_map:                                         #As long as bot is valid
            if bot == args.p1:                                      #If bot is player 1
                p1 = bot_map[args.p1](Board.PLAYER1_PIECE)          #Set bot as player 1
        if p1 is None:                                              #If there is no player 1 still
            print("oops! you have entered a wrong bot name for p1") #Print this and exit program
            exit(1)                                                 
        print("Player 1 is set as a " + name_map[args.p1])          #Else print bot is set as player 1

    if args.p2 is None or args.p2 == "human":                       #Checks if human is player 2
        print("Player 2 is set as a Human")
        p2 = Human(Board.PLAYER2_PIECE)                             #Set human as player 2
    else:                                                           #If not the case
        for bot in bot_map:                                         #As long as bot is valid
            if bot == args.p2:                                      #If bot is player 2
                p2 = bot_map[args.p2](Board.PLAYER2_PIECE)          #Set bot as player 2
        if p2 is None:                                              #If there is no player 2 still
            print("oops! you have entered a wrong bot name for p2") #Print this and exit program
            exit(1)
        print("Player 2 is set as a " + name_map[args.p2])          #Else print bot is set as player 2

    print("\n")

    if args.ui == False and (Human == type(p1) or Human == type(p2)):   #Case there is no UI while human
        print("Can not play game as Human without UI!")
        exit(1)

    connect4(p1, p2, args.ui)                                       #Begin the connect 4 game with ui


"""
Function Name: main_screen
Precondition: None
Postcondition: Will display main screen UI

Description: 
This function provides the main menu UI state.
"""
def main_screen():
    pygame.init()                                                   #initialize all imported pygame modules
    pygame.display.set_caption("Connect Four")                      #sets the ui name as connect four
    # board = Board(1)
    graphics_board = GBoard(board)                                  #initialize the graphic board

    """
    Function name: human_vs_human
    Precondition: User clicks human vs human button
    Postcondition: Moves to human to human board state
    
    Description: In the case the user clicks the human vs human button
    This function is called and moves the UI state to the connect 4 state.
    """
    def human_vs_human():
        main("human", "human")

    player_vs_player_button = graphics_board.create_button(60, 220, 300, 40, '1. PLAYER VS PLAYER', human_vs_human)         #button for human vs human option
    player_vs_bot_button = graphics_board.create_button(60, 280, 300, 40, '2. PLAYER VS BOT', bot_vs_human_screen)          #button for human vs bot option
    bot_vs_bot_button = graphics_board.create_button(60, 340, 300, 40, '3. BOT VS BOT', bot_vs_bot_screen)                  #button for bot vs bot option
    quit_button = graphics_board.create_button(60, 600, 100, 40, 'QUIT', sys.exit)                                          #button for quit option

    button_list = [player_vs_player_button, player_vs_bot_button, bot_vs_bot_button, quit_button]                           #list to hold buttons

    while True:         #keep this state open until user clicks a button
        graphics_board.write_on_board("CONNECT 4", graphics_board.BLUE , 350 , 100, 60, True)                               #Writes title on UI
        graphics_board.write_on_board("CHOOSE ONE OF THE OPTIONS TO PLAY", graphics_board.YELLOW , 350 , 175, 30, True)     #writes prompt on UI

        for event in pygame.event.get():                                        #getting user clicks
            if event.type == pygame.QUIT:                                       #if user quit, exit program
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:                          #checks where user clicks
                if event.button == 1:                                           #if the user clicked on button
                    for button in button_list:
                        if button['button position'].collidepoint(event.pos):   #have the system move to option
                            button['callback']()
            
            elif event.type == pygame.MOUSEMOTION:                              #follows the mouse motion
                for button in button_list:
                    if button['button position'].collidepoint(event.pos):
                        button['color'] = graphics_board.RED
                    else:
                        button['color'] = graphics_board.WHITE

        for button in button_list:                                              #draws buttons onto UI
            graphics_board.draw_button(button, graphics_board.screen)

        pygame.display.update()

"""
Function Name: bot_vs_human_screen
Precondition: User clicks on bot_vs_human button
Postcondition: Will display main screen UI

Description: 
This function provides the main menu UI state.
"""
def bot_vs_human_screen():
    pygame.init()                           #initialize all imported pygame modules
    graphics_board = GBoard(board)          #initialize the graphic board

    """
    Function name: human_vs_minimax
    Precondition: User clicks human vs minimax button
    Postcondition: Moves to human to minimax board state
    
    Description: In the case the user clicks the human vs minimax button
    This function is called and moves the UI state to the connect 4 state.
    """
    def human_vs_minimax():
        main("human", "minimax")
        
        
    """
    Function name: human_vs_montecarlo
    Precondition: User clicks human vs montecarlo button
    Postcondition: Moves to human to minimax board state
    
    Description: In the case the user clicks the human vs montecarlo button
    This function is called and moves the UI state to the connect 4 state.
    """    
    def human_vs_montecarlo():
        main("human", "montecarlo")

    minimax_button = graphics_board.create_button(60, 220, 400, 40, '1. MINIMAX BOT', human_vs_minimax)                     #button for human_vs_minimax
    montecarlo_button = graphics_board.create_button(60, 280, 400, 40, '2. MONTECARLO SEARCH BOT', human_vs_montecarlo)     #button for human_vs_montecarlo
    
    back_button = graphics_board.create_button(60, 600, 100, 40, 'BACK', main_screen)                                       #button for back 
    quit_button = graphics_board.create_button(180, 600, 100, 40, 'QUIT', sys.exit)                                         #button for quit

    button_list = [minimax_button, montecarlo_button, back_button, quit_button]                                             #list to hold buttons

    while True:         #keep state open
        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)                           #Writes title on UI
        graphics_board.write_on_board("CHOOSE THE BOT TO PLAY AGAINST", graphics_board.YELLOW , 350 , 175, 30, True)        #writes prompt on UI

        for event in pygame.event.get():                                         #getting user clicks
            if event.type == pygame.QUIT:                                        #if user quit, exit program
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:                           #checks where user clicks
                if event.button == 1:                                            #if the user clicked on button
                    for button in button_list:
                        if button['button position'].collidepoint(event.pos):    #have the system move to option
                            button['callback']()
            
            elif event.type == pygame.MOUSEMOTION:                               #follows the mouse motion
                for button in button_list:
                    if button['button position'].collidepoint(event.pos):
                        button['color'] = graphics_board.RED
                    else:
                        button['color'] = graphics_board.WHITE

        for button in button_list:
            graphics_board.draw_button(button, graphics_board.screen)            #draws buttons onto UI

        pygame.display.update()


"""
Function Name: bot_vs_bot_screen
Precondition: User clicks on bot_vs_bot button
Postcondition: Moves to bot vs bot board state

Description: 
This function is the bot vs bot screen
"""
def bot_vs_bot_screen():
    pygame.init()                                       #initialize all imported pygame modules
    # board = Board(1)
    graphics_board = GBoard(board)                      #initialize the graphic board

    first_bot = second_bot = None                       #set bots to none

    """
    Function Name: bot_to_play_against
    Precondition: user clicks on bot button
    Postcondition: bot is positioned as first or second bot

    Description: 
    This function assigns chosen bots to play connect4
    """
    def bots_to_play_against(bot_to_play):
        nonlocal first_bot, second_bot                  #nonlocal variables

        if first_bot == None:                           #if first bot not chosen yet
            first_bot = bot_to_play                     #assign user chosen bot as first bot
        elif second_bot == None and first_bot != None:  #if first bot is chosen but not second bot chosen
            second_bot= bot_to_play                     #assign user chosen bot as second bot

        if first_bot != None and second_bot != None:    #if both bots have been chosen
            main(first_bot, second_bot)                 #go to main function with both chosen bots

    minimax_button = graphics_board.create_button(60, 220, 400, 40, '1. MINIMAX BOT',  bots_to_play_against, ("minimax"))                   #buttton for minimax
    montecarlo_button = graphics_board.create_button(60, 280, 400, 40, '2. MONTECARLO SEARCH BOT', bots_to_play_against, ("montecarlo"))    #button for montecarlo
    
    back_button = graphics_board.create_button(60, 600, 100, 40, 'BACK', main_screen)                                                       #button for back
    quit_button = graphics_board.create_button(180, 600, 100, 40, 'QUIT', sys.exit)                                                         #button for quit

    button_list = [minimax_button, montecarlo_button, back_button, quit_button]                                                             #list to hold button

    while True:     #keep state open
        graphics_board.write_on_board("CONNECT 4 GAME", graphics_board.RED , 350 , 100, 60, True)                                           #Writes title on UI
        graphics_board.write_on_board("CHOOSE ANY TWO BOT(S) TO PLAY", graphics_board.YELLOW , 350 , 175, 30, True)                         #writes prompt on UI

        for event in pygame.event.get():                                        #getting user clicks
            if event.type == pygame.QUIT:                                       #if user quit, exit program
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:                          #checks where user clicks
                if event.button == 1:                                           #if the user clicked on button
                    for button in button_list:
                        if button['button position'].collidepoint(event.pos):   #have the system move to option
                            if(button['args'] != None):
                                button['callback'](button['args'])
                            else:
                                button['callback']()
            
            elif event.type == pygame.MOUSEMOTION:                              #follows the mouse motion
                for button in button_list:
                    if button['button position'].collidepoint(event.pos):
                        button['color'] = graphics_board.RED
                    else:
                        button['color'] = graphics_board.WHITE                
        
        for button in button_list:
            graphics_board.draw_button(button, graphics_board.screen)           #draws buttons onto UI

        pygame.display.update()

if __name__ == '__main__':
    main()
