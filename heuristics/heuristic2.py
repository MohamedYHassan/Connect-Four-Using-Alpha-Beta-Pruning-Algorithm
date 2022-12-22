import numpy as np
import random
import pygame
import sys
import math


BLACK = (0,0,0)
BLUE = (15,82,186)
YELLOW = (210,181,91)
RED = (184,15,10)

ROWS = 6
COLS = 7

HUMAN = 0
AI = 1
WINNER = -1

EMPTY = 0
HUMAN_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 2


def create_board():
	board = np.zeros((ROWS,COLS))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
	for row in range(ROWS):
		if board[row][col] == 0:
			return row

def print_board(board):
	print(np.flip(board, 0))

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


	
	if window.count(piece) == 2:
		score += 100




	

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

def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def draw_board(board):
	for col in range(COLS):
		for row in range(ROWS):
			pygame.draw.rect(screen, YELLOW, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for col in range(COLS):
		for row in range(ROWS):		
			if board[row][col] == HUMAN_PIECE:
				pygame.draw.circle(screen, RED, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[row][col] == AI_PIECE: 
				pygame.draw.circle(screen, BLUE, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 90

width = COLS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 10)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("courier", 75)

turn = random.randint(HUMAN, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			x = event.pos[0]
			if turn == HUMAN:
				pygame.draw.circle(screen, RED, (x, int(SQUARESIZE/2)), RADIUS)

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

					if winning_move(board, HUMAN_PIECE):
						label = font.render("You Win!", 1, RED)
						screen.blit(label, (40,10))
						WINNER = HUMAN
						game_over = True

					turn += 1
					turn = turn % 2
					

					print_board(board)
					draw_board(board)


	# Player 2 
	if turn == AI and not game_over:				

		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = font.render("AI Wins!", 1, YELLOW)
				screen.blit(label, (40,10))
				WINNER = AI
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if get_valid_locations(board) == []:
		game_over = True
			

	if game_over:
		if WINNER == -1:
			label = font.render("Draw!", 1, YELLOW)
			screen.blit(label, (40,10))
			print_board(board)
			draw_board(board)
			pygame.display.update()
		pygame.time.wait(3000)
		