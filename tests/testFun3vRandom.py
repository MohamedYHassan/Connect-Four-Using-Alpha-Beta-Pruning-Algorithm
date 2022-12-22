import numpy as np
import random
import pygame
import sys
import math

BLUE = (15,82,186)
BLACK = (0,0,0)
RED = (184,15,10)
YELLOW = (210,181,91)

ROW_COUNT = 6
COLUMN_COUNT= 7

HUMAN = 0
AI = 1
winner = -1

EMPTY = 0
AI_1 = 1
AI_2 = 2

WINDOW_LENGTH = 4
WINDOW_LENGTH2 = 2

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True







def evaluate_window(window, piece):
	score = 0
	opp_piece = AI_2
	

	if window.count(opp_piece) == 4:
		score -= 100

	

	return score





def score_position(board, piece):
	score = 0

	##  Center 
	#center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	#center_count = center_array.count(piece)
	#score += center_count * 3

	##  Horizontal
	for row in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[row,:])]
		for col in range(COLUMN_COUNT-3):
			window = row_array[col:col+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	##  Vertical
	for col in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,col])]
		for row in range(ROW_COUNT-3):
			window = col_array[row:row+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	##  Diagonal
	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			window = [board[row+i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			window = [board[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score





def evaluate_window2(window, piece):
	score = 0
	opp_piece = AI_1
	if piece == AI_1:
		opp_piece = AI_2

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 10


	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 20

	

	return score





def score_position2(board, piece):
	score = 0

	##  Center 
	#center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	#center_count = center_array.count(piece)
	#score += center_count * 3

	##  Horizontal
	for row in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[row,:])]
		for col in range(COLUMN_COUNT-3):
			window = row_array[col:col+WINDOW_LENGTH]
			score += evaluate_window2(window, piece)

	##  Vertical
	for col in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,col])]
		for row in range(ROW_COUNT-3):
			window = col_array[row:row+WINDOW_LENGTH]
			score += evaluate_window2(window, piece)

	##  Diagonal
	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			window = [board[row+i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window2(window, piece)

	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			window = [board[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window2(window, piece)

	return score




def is_terminal_node(board):
	return winning_move(board, AI_1) or winning_move(board, AI_2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_1):
				return (None, 100000000000000)
			elif winning_move(board, AI_2):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_1))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_1)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_2)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value



def minimax2(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_2):
				return (None, 100000000000000)
			elif winning_move(board, AI_1):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position2(board, AI_2))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_2)
			new_score = minimax2(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_1)
			new_score = minimax2(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
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
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, YELLOW, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == AI_1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_2: 
				pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 90

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 10)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("courier", 75)

turn = random.randint(HUMAN, AI)
counter1 = 0
counter2 = 0

while not game_over:


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

	#	if event.type == pygame.MOUSEMOTION:
	#		pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
	#		posx = event.pos[0]
	#		if turn == HUMAN:
	#			pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

	#	pygame.display.update()

	#	if event.type == pygame.MOUSEBUTTONDOWN:
	#		pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

			# Player 1 Input
	if turn == HUMAN:
		if counter1 == 0 or counter1 == 1 :
			
			col = random.randint(0, COLUMN_COUNT-1)

		else:


		#posx = event.pos[0]
		#		col = int(math.floor(posx/SQUARESIZE))
			col,minimax_score=minimax(board,3,-math.inf,math.inf,True)

		if is_valid_location(board, col):
			pygame.time.wait(300)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_1)

			if winning_move(board, AI_1):
				label = font.render("AI 1 Wins!", 1, RED)
				screen.blit(label, (40,10))
				winner = HUMAN
				game_over = True

			turn += 1
			turn = turn % 2
			counter1 = counter1 + 1		

			print_board(board)
			draw_board(board)


	# Player 2 Input
	if turn == AI and not game_over:	
		if counter2 == 0 or counter2 == 1:
		
			col = random.randint(0, COLUMN_COUNT-1)

		else:
			#col = pick_best_move(board, AI_2)
			col = random.randint(0, COLUMN_COUNT-1)

		if is_valid_location(board, col):
			pygame.time.wait(300)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_2)

			if winning_move(board, AI_2):
				label = font.render("AI 2 Wins!", 1,BLUE)
				screen.blit(label, (40,10))
				winner = AI
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2
			counter2 = counter2 + 1

	if get_valid_locations(board) == []:
		game_over = True
			

	if game_over:
		if winner == -1:
			label = font.render("Draw!", 1, YELLOW)
			screen.blit(label, (40,10))
			print_board(board)
			draw_board(board)
			pygame.display.update()
		pygame.time.wait(3000)
