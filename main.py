import numpy as np
import random
import pygame
import sys
import math
from button import Button
import threading


BLACK = (0,0,0)
BLUE = (15,82,186)
YELLOW = (210,181,91)
RED = (184,15,10)
BG = pygame.image.load("pics/Background.png")

ROWS = 6
COLS = 7

HUMAN = 0
AI = 1


EMPTY = 0
HUMAN_PIECE = 1
AI_PIECE = 2


GAME_OVER = False

WINDOW_LENGTH = 4



def create_board():
    board = np.zeros((ROWS,COLS))
    return board

def print_board(board):
    print(np.flip(board, 0))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row



def winning_move(board, piece):
    #  horizontal 
    for col in range(COLS-3):
        for row in range(ROWS):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    #  vertical 
    for col in range(COLS):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    #  positive diaganols
    for col in range(COLS-3):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    #  negative diaganols
    for col in range(COLS-3):
        for row in range(3, ROWS):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = HUMAN_PIECE
    if piece == HUMAN_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10

    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 4

    if window.count(opp_piece) == 4:
        score -= 100
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 20

    

    return score





def score_position(board, piece):
    score = 0

    ##  Center 
    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ##  Horizontal
    for row in range(ROWS):
        row_array = [int(i) for i in list(board[row,:])]
        for col in range(COLS-3):
            window = row_array[col:col+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ##  Vertical
    for col in range(COLS):
        col_array = [int(i) for i in list(board[:,col])]
        for row in range(ROWS-3):
            window = col_array[row:row+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ##  Diagonal
    for row in range(ROWS-3):
        for col in range(COLS-3):
            window = [board[row+i][col+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for row in range(ROWS-3):
        for col in range(COLS-3):
            window = [board[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score





def is_terminal_node(board):
    return winning_move(board, HUMAN_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, HUMAN_PIECE):
                return (None, -10000000000000)
            else: # Game over, no more moves
                return (None, 0)
        else: # Depth = 0
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing 
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, HUMAN_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value





def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations



def draw_board(board,human_colour,ai_colour):
    for col in range(COLS):
        for row in range(ROWS):
            pygame.draw.rect(screen, YELLOW, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for col in range(COLS):
        for row in range(ROWS):     
            if board[row][col] == HUMAN_PIECE:
                pygame.draw.circle(screen, human_colour, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[row][col] == AI_PIECE: 
                pygame.draw.circle(screen, ai_colour, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


    









pygame.init()
music = pygame.mixer.music.load("sound effects/background.mp3")
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound("sound effects/select.mp3")
tick = pygame.mixer.Sound("sound effects/tick.mp3")
win = pygame.mixer.Sound("sound effects/win.mp3")
lose = pygame.mixer.Sound("sound effects/lose.mp3")
draw = pygame.mixer.Sound("sound effects/draw.mp3")



SQUARESIZE = 100

width = COLS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE

size = (width,height)

RADIUS = int(SQUARESIZE/2 - 10)

screen = pygame.display.set_mode(size)



font = pygame.font.SysFont("courier", 75)







def get_font(size): 
    return pygame.font.Font("pics/font.ttf", size)


   


def main_menu():
    pygame.display.set_caption("Menu")
    condition = True
    

    try:

        while condition:
            screen.blit(BG,(0,0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(350,100))

            PLAY_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250), 
                                text_input="PLAY AI", font=get_font(35), base_color="#d7fcd4", hovering_color="Yellow")

            PLAY_LOCAL_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 400), 
                                text_input="PLAY FRIEND", font=get_font(30), base_color="#d7fcd4", hovering_color="Yellow")
            
            QUIT_BUTTON = Button(image=pygame.image.load("pics/Quit Rect.png"), pos=(350, 550), 
                                text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="Yellow")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, PLAY_LOCAL_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        choose_color()
                    if PLAY_LOCAL_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        choose_color2()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        condition = False
                        
                        

            pygame.display.update()

        exit()
        

    except SystemExit:
        pygame.quit()


def choose_color():
    pygame.display.set_caption("Game")
    screen.fill("black")


    try:
        while True:
            screen.blit(BG,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(50).render("CHOOSE COLOUR", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350,100))

            RED_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250), 
                            text_input="RED", font=get_font(40), base_color=RED, hovering_color="Red")
            BLUE_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 450), 
                            text_input="BLUE", font=get_font(40), base_color=BLUE, hovering_color="Blue")


            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350,650),text_input="BACK",font=get_font(40), base_color="Yellow", hovering_color="Green")
            


            for button in [RED_BUTTON, BLUE_BUTTON,BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if RED_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        human_colour = RED
                        ai_colour = BLUE
                        choose_difficulty(human_colour,ai_colour)
                    if BLUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        human_colour = BLUE
                        ai_colour = RED
                        choose_difficulty(human_colour,ai_colour)

                    if BACK.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        main_menu()

                    

            pygame.display.update()
    except SystemExit:
        pygame.quit()




def choose_color2():
    pygame.display.set_caption("Game")
    screen.fill("black")


    try:
        while True:
            screen.blit(BG,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(45).render("PLAYER 1 COLOUR", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350,100))

            RED_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250), 
                            text_input="RED", font=get_font(40), base_color=RED, hovering_color="Red")
            BLUE_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 450), 
                            text_input="BLUE", font=get_font(40), base_color=BLUE, hovering_color="Blue")


            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350,650),text_input="BACK",font=get_font(40), base_color="Yellow", hovering_color="Green")
            


            for button in [RED_BUTTON, BLUE_BUTTON,BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if RED_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        human_colour = RED
                        ai_colour = BLUE
                        play2(human_colour,ai_colour)
                    if BLUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        human_colour = BLUE
                        ai_colour = RED
                        play2(human_colour,ai_colour)

                    if BACK.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        main_menu()

                    

            pygame.display.update()
    except SystemExit:
        pygame.quit()






def choose_difficulty(human_colour,ai_colour):
    pygame.display.set_caption("Game")
    screen.fill("black")


    try:

        while True:
            screen.blit(BG,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(50).render("CHOOSE LEVEL", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350,100))

            EASY_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 230), 
                                text_input="EASY", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")
            MEDIUM_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 380), 
                                text_input="MEDIUM", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")
            HARD_BUTTON = Button(image=pygame.image.load("pics/Quit Rect.png"), pos=(350, 530), 
                                text_input="HARD", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")

            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350,650),text_input="BACK",font=get_font(40), base_color="Yellow", hovering_color="Green")

            for button in [EASY_BUTTON, MEDIUM_BUTTON,HARD_BUTTON,BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        
                        level = 1
                        play(level,human_colour,ai_colour)
                    if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                       
                        level = 3
                        play(level,human_colour,ai_colour)
                    if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        
                        level = 5
                        play(level,human_colour,ai_colour)

                    if BACK.checkForInput(MENU_MOUSE_POS):
                        click.play()
                        choose_color()
                    

            pygame.display.update()
    except SystemExit:
        pygame.quit()



def play2(human_colour,ai_colour):
    pygame.mixer.music.set_volume(0.4)
    
    pygame.display.set_caption("Game")
    screen.fill("black")
    board = create_board()
    print_board(board)
    turn = random.randint(HUMAN, AI)
    GAME_OVER = False
    WINNER = -1


    
    while not GAME_OVER:

        draw_board(board,human_colour,ai_colour)
    #pygame.display.update()

    



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                x = event.pos[0]
                if turn == HUMAN:
                    pygame.draw.circle(screen, human_colour, (x, int(SQUARESIZE/2)), RADIUS)
                elif turn == AI:
                    pygame.draw.circle(screen, ai_colour, (x, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

                # Player 1 
                if turn == HUMAN:
                    x = event.pos[0]
                    col = int(math.floor(x/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, HUMAN_PIECE)
                        tick.play()

                        if winning_move(board, HUMAN_PIECE):
                            pygame.mixer.music.pause()
                            win.play()
                            label = font.render("Player 1 Wins!", 1, human_colour)
                            screen.blit(label, (40,10))
                            WINNER = HUMAN

                            GAME_OVER = True

                        turn += 1
                        turn = turn % 2
                    
                        print_board(board)
                        draw_board(board,human_colour,ai_colour)


        # Player 2 
                elif turn == AI and not GAME_OVER:                

                    x = event.pos[0]
                    col = int(math.floor(x/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, AI_PIECE)
                        tick.play()

                        if winning_move(board, AI_PIECE):
                            pygame.mixer.music.pause()
                            win.play()
                            label = font.render("Player 2 Wins!", 1, ai_colour)
                            screen.blit(label, (40,10))
                            WINNER = AI

                            GAME_OVER = True

                        turn += 1
                        turn = turn % 2
                    
                        print_board(board)
                        draw_board(board,human_colour,ai_colour)

                        

                if get_valid_locations(board) == []:
                    GAME_OVER = True
            

                if GAME_OVER:
                    if WINNER == -1:
                        pygame.mixer.music.pause()
                        draw.play()
                        label = font.render("Draw!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        print_board(board)
                        draw_board(board,human_colour,ai_colour)
                        pygame.display.update()
                    pygame.time.wait(5000)
                    pygame.mixer.music.unpause()
                    main_menu()
    
    pygame.quit()
    sys.exit()





def play(level,human_colour,ai_colour):
    pygame.mixer.music.set_volume(0.4)
    print(level)
    pygame.display.set_caption("Game")
    screen.fill("black")
    board = create_board()
    print_board(board)
    turn = random.randint(HUMAN, AI)
    GAME_OVER = False
    WINNER = -1
    draw_board(board,human_colour,ai_colour)

    
    while not GAME_OVER:

        
    #pygame.display.update()

    



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                x = event.pos[0]
                if turn == HUMAN:
                    pygame.draw.circle(screen, human_colour, (x, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

                # Player 1 
                if turn == HUMAN:
                    x = event.pos[0]
                    col = int(math.floor(x/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, HUMAN_PIECE)
                        tick.play()

                        if winning_move(board, HUMAN_PIECE):
                            pygame.mixer.music.pause()
                            win.play()
                            label = font.render("You Win!", 1, human_colour)
                            screen.blit(label, (40,10))
                            WINNER = HUMAN

                            GAME_OVER = True

                        turn += 1
                        turn = turn % 2
                    
                        print_board(board)
                        draw_board(board,human_colour,ai_colour)


        # Player 2 
        if turn == AI and not GAME_OVER:                

            col, minimax_score = minimax(board, level, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                tick.play()

                if winning_move(board, AI_PIECE):
                    pygame.mixer.music.pause()
                    lose.play()
                    label = font.render("AI Wins!", 1, ai_colour)
                    screen.blit(label, (40,10))
                    WINNER = AI
                    GAME_OVER = True

                print_board(board)
                draw_board(board,human_colour,ai_colour)

                turn += 1
                turn = turn % 2

                if get_valid_locations(board) == []:
                    GAME_OVER = True
            

                if GAME_OVER:
                    if WINNER == -1:
                        pygame.mixer.music.pause()
                        draw.play()
                        label = font.render("Draw!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        print_board(board)
                        draw_board(board,human_colour,ai_colour)
                        pygame.display.update()
                    pygame.time.wait(5000)
                    pygame.mixer.music.unpause()
                    main_menu()
    
    pygame.quit()
    sys.exit()
    





try:
    main_menu()
except SystemExit:
    pygame.quit()




        
