import pygame,math
import time
from pygame.locals import*

pygame.init()
FPS = 30
fpsClock = pygame.time.Clock()

# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 
# light shade of the button 
color_light = (170,170,170) 
  
# dark shade of the button 
color_dark = (100,100,100) 
# rendering a text written in 
# this font 
text = smallfont.render('New game' , True , (255,255,255)) 

dis = pygame.display.set_mode((470, 470)) #kích thước 600x500
pygame.display.set_caption('Co ganh')
icon = pygame.image.load('img/Ganh_Chess1.jpg')
pygame.display.set_icon(icon)

map = pygame.image.load('img/map.jpg')
# Tạo các quân cờ
red = pygame.image.load('img/red.png')
blue = pygame.image.load('img/blue.png')
yellow = pygame.image.load('img/yellow.png')
lose = pygame.image.load('img/lose-removebg-preview.png')
win = pygame.image.load('img/win-removebg-preview.png')

# Đặt chỉ số quân cờ
chess = {1: blue, -1 : red
		}

# Khởi tạo bàn cờ
matrix  = [
			[0, 0, 0, 0, 0, 0],
			[0,-1,-1,-1, 1, 1],
			[0,-1, 0, 0, 0, 1],
			[0,-1, 0, 0, 0, 1],
			[0,-1, 0, 0, 0, 1],
			[0,-1,-1, 1, 1, 1]
]
row = [0]
column = [0]

### xếp quân lên bàn cờ
def location():
	global row, column
	lx = 12
	ly = 12
	for x in range(1,6):
		row.append(lx)
		lx += 105
	for y in range(1,6):
		column.append(ly)
		ly += 105

# Đếm số quân cờ
def num(chess):
	num = 0 
	for y in range(1,6):
			for x in range(1,6):
				if matrix[x][y] == chess :
					num += 1
	return num

def xepquan():	
	for b in range(6):
		for a in range(6):
			if matrix[a][b]!=0 :
				dis.blit(chess[matrix[a][b]],(column[a],row[b]))

# Xét click chuột
def mouse_stay():
	if(12 <= xmouse <= 440) and (12 <= ymouse <= 440):
		for y in range(1,6):
			for x in range(1,6):
				if(row[x] <= xmouse <= row[x] + 105) and (column[y] <= ymouse <= column[y] + 105):
					return [x,y]
	return [0,0]				

# Các vị trí có thể đi tại 1 vị trí xét

def possible(chess,x,y):
	result = []
	if y != 5:
		if matrix[x][y+1] == 0 :result.append([x,y+1])
	if y != 1:
		if matrix[x][y-1] == 0: result.append([x,y-1])
	if x != 1:
		if matrix[x-1][y] == 0: result.append([x-1,y])
	if x != 5:
		if matrix[x+1][y] == 0: result.append([x+1,y])
	if (y % 2 == 1 and x % 2 == 1) or (y % 2 == 0 and x % 2 == 0) : 
		if y != 5 and x != 5 :
			if matrix[x+1][y+1] == 0 :result.append([x+1,y+1])
		if y != 1 and x != 1 :
			if matrix[x-1][y-1] == 0: result.append([x-1,y-1])
		if x != 1 and y != 5 :
			if matrix[x-1][y+1] == 0: result.append([x-1,y+1])
		if x != 5 and y != 1 :
			if matrix[x+1][y-1] == 0: result.append([x+1,y-1])
	return result

def checkaround(chess,x,y):
	result = []
	if y != 5:
		if matrix[x][y+1] == -chess: result.append([x,y+1])
	if y != 1:
		if matrix[x][y-1] == -chess: result.append([x,y-1])
	if x != 1:
		if matrix[x-1][y] == -chess: result.append([x-1,y])
	if x != 5:
		if matrix[x+1][y] == -chess: result.append([x+1,y])
	if (y % 2 == 1 and x % 2 == 1) or (y % 2 == 0 and x % 2 == 0) : 
		if y != 5 and x != 5 :
			if matrix[x+1][y+1] == -chess :result.append([x+1,y+1])
		if y != 1 and x != 1 :
			if matrix[x-1][y-1] == -chess: result.append([x-1,y-1])
		if x != 1 and y != 5 :
			if matrix[x-1][y+1] == -chess: result.append([x-1,y+1])
		if x != 5 and y != 1 :
			if matrix[x+1][y-1] == -chess: result.append([x+1,y-1])
	return result

def checkbay():
	global before_move
	result = False
	i = before_move[0]
	j = before_move[1]
	chess = matrix[before_move[2]][before_move[3]]
	if(i != 5):
		if (matrix[i+1][j] == chess) and (matrix[i-1][j] == chess) :
			result = True
	if(j != 5):
		if (matrix[i][j+1] == chess) and (matrix[i][j-1] == chess) :
			result = True
	if (i, j)==(2, 2) or (i, j) == (3, 3) or (i, j) == (4, 4) or (i, j) == (4, 2) or (i, j) == (2, 4) : 
		if (matrix[i+1][j+1] ==chess) and (matrix[i-1][j-1] == chess) :
			result = True
		if (matrix[i-1][j+1] == chess) and (matrix[i+1][j-1] == chess) :
			result = True
	return result 
			
def bay(x,y):
	global before_move
	i = before_move[0]
	j = before_move[1]
	chess = matrix[before_move[2]][before_move[3]]
	if (len(checkaround(chess,i,j)) > 0) and checkbay():
		if [x,y] in checkaround(chess,i,j) :
			print([i,j])
			return [i,j]
		else:
			return [0]
	else : 
		print(checkaround(chess,i,j))
		return []

#################################################################################################
def show_move(ListPosition):
	if ListPosition != []:
		for i in range(len(ListPosition)):
			x = ListPosition[i][0]
			y = ListPosition[i][1]
			dis.blit(yellow,(column[x],row[y]))
# Di chuyển
this_chessIMG = 0
after = 0; before = 0
wChess,hChess = red.get_size()
ListPosition = []
chessColor = 0
def move():
	global chessColor, after, before, this_chessIMG, ListPosition,before_move
	if click != [0,0] and change :
		if click[0]:
			ListPosition = []
			before = Block_current
			chessColor = matrix[before[0]][before[1]]
			this_chessIMG = chess[chessColor]
			
			if not before_move :
				ListPosition = possible(chessColor,before[0],before[1])
			else:
				if len(bay(before[0],before[1])) > 0 :
					if len(bay(before[0],before[1])) == 1 :
						ListPosition = []
					else :
						ListPosition.append([before_move[0],before_move[1]])
				else :
					ListPosition = possible(chessColor, before[0], before[1])

			matrix[before[0]][before[1]] = 0
		else:
			after = Block_current

			if [after[0],after[1]] in ListPosition : 
				matrix[after[0]][after[1]] = chessColor
				this_chessIMG = 0

				if(after[0] != 5):
					if (matrix[after[0]+1][after[1]] == -chessColor) and (matrix[after[0]-1][after[1]] == -chessColor) :
						matrix[after[0]+1][after[1]] = chessColor
						matrix[after[0]-1][after[1]] = chessColor
				if(after[1] != 5):
					if (matrix[after[0]][after[1]+1] == -chessColor) and (matrix[after[0]][after[1]-1] == -chessColor) :
						matrix[after[0]][after[1]+1] = chessColor
						matrix[after[0]][after[1]-1] = chessColor
				if (after[0], after[1])==(2, 2) or (after[0], after[1]) == (3, 3) or (after[0], after[1]) == (4, 4) or (after[0], after[1]) == (4, 2) or (after[0], after[1]) == (2, 4) : 
					if (matrix[after[0]+1][after[1]+1] == -chessColor) and (matrix[after[0]-1][after[1]-1] == -chessColor) :
						matrix[after[0]+1][after[1]+1] = chessColor
						matrix[after[0]-1][after[1]-1] = chessColor
					if (matrix[after[0]-1][after[1]+1] == -chessColor) and (matrix[after[0]+1][after[1]-1] == -chessColor) :
						matrix[after[0]-1][after[1]+1] = chessColor
						matrix[after[0]+1][after[1]-1] = chessColor
				before_move = [before[0],before[1],after[0],after[1]]

				dis.fill((255,255,255))
				dis.blit(map,(20,20))
				xepquan()
				change_turn()
			else : 
				matrix[before[0]][before[1]] = chessColor

	if this_chessIMG != 0 :
		dis.fill((255,255,255))
		dis.blit(map,(20,20)) 
		show_move(ListPosition)
		xepquan()
		if matrix[before[0]][before[1]] != chessColor :
			dis.blit(this_chessIMG,(xmouse - wChess//2,ymouse - hChess//2))

def nextClick():
	if Click1 : 
		return False,True		
	else : return True,False

##################### Tao AI cho may 

def get_way(matrix, isPlayer, move) :
	all_ways = [];
	before = [move[0],move[1]]
	after = [move[2],move[3]]
	result = []
	i = move[0]
	j = move[1]

	chess = matrix[move[2]][move[3]]

	if checkaround(chess,i,j):
		for y in range(1,6) :
			for x in range(1,6) :
				if matrix[x][y] != 0 :
					if [x,y] in checkaround(chess,i,j) and matrix[x][y] == -chess:
						if(i != 5):
							if (matrix[i+1][j] == chess) and (matrix[i-1][j] == chess) :
								all_ways.append([x,y,i,j])
							
						if(j != 5):
							if (matrix[i][j+1] == chess) and (matrix[i][j-1] == chess) :
								all_ways.append([x,y,i,j])
						
						if (i, j)==(2, 2) or (i, j) == (3, 3) or (i, j) == (4, 4) or (i, j) == (4, 2) or (i, j) == (2, 4) : 
							if (matrix[i+1][j+1] == chess) and (matrix[i-1][j-1] == chess) :
								all_ways.append([x,y,i,j])
								
							if (matrix[i-1][j+1] == chess) and (matrix[i+1][j-1] == chess) :
								all_ways.append([x,y,i,j])	
													
	if not all_ways : 
		for y in range(1,6) :
			for x in range(1,6) : 
				if isPlayer and matrix[x][y] < 0 :
					if y != 5:
						if matrix[x][y+1] == 0 :all_ways.append([x,y,x,y+1])
					if y != 1:
						if matrix[x][y-1] == 0: all_ways.append([x,y,x,y-1])
					if x != 1:
						if matrix[x-1][y] == 0: all_ways.append([x,y,x-1,y])
					if x != 5:
						if matrix[x+1][y] == 0: all_ways.append([x,y,x+1,y])
					if (y % 2 == 1 and x % 2 == 1) or (y % 2 == 0 and x % 2 == 0) : 
						if y != 5 and x != 5 :
							if matrix[x+1][y+1] == 0 :all_ways.append([x,y,x+1,y+1])
						if y != 1 and x != 1 :
							if matrix[x-1][y-1] == 0: all_ways.append([x,y,x-1,y-1])
						if x != 1 and y != 5 :
							if matrix[x-1][y+1] == 0: all_ways.append([x,y,x-1,y+1])
						if x != 5 and y != 1 :
							if matrix[x+1][y-1] == 0: all_ways.append([x,y,x+1,y-1])
				elif not isPlayer and matrix[x][y] > 0 :
					if y != 5:
						if matrix[x][y+1] == 0 :all_ways.append([x,y,x,y+1])
					if y != 1:
						if matrix[x][y-1] == 0: all_ways.append([x,y,x,y-1])
					if x != 1:
						if matrix[x-1][y] == 0: all_ways.append([x,y,x-1,y])
					if x != 5:
						if matrix[x+1][y] == 0: all_ways.append([x,y,x+1,y])
					if (y % 2 == 1 and x % 2 == 1) or (y % 2 == 0 and x % 2 == 0) : 
						if y != 5 and x != 5 :
							if matrix[x+1][y+1] == 0 :all_ways.append([x,y,x+1,y+1])
						if y != 1 and x != 1 :
							if matrix[x-1][y-1] == 0: all_ways.append([x,y,x-1,y-1])
						if x != 1 and y != 5 :
							if matrix[x-1][y+1] == 0: all_ways.append([x,y,x-1,y+1])
						if x != 5 and y != 1 :
							if matrix[x+1][y-1] == 0: all_ways.append([x,y,x+1,y-1])
	return all_ways
	

def move_not_real(move,newMatrix) :
	
	swapchess = []
	before = [move[0],move[1]]
	after = [move[2],move[3]]
	chessColor = newMatrix[before[0]][before[1]]
	newMatrix[before[0]][before[1]] = 0
	newMatrix[after[0]][after[1]] = chessColor

	if(after[0] != 5):
		if (newMatrix[after[0]+1][after[1]] == -chessColor) and (newMatrix[after[0]-1][after[1]] == -chessColor) :
			newMatrix[after[0]+1][after[1]] = chessColor
			newMatrix[after[0]-1][after[1]] = chessColor
			swapchess.append([after[0]+1,after[1]])
			swapchess.append([after[0]-1,after[1]])
	if(after[1] != 5):
		if (newMatrix[after[0]][after[1]+1] == -chessColor) and (newMatrix[after[0]][after[1]-1] == -chessColor) :
			newMatrix[after[0]][after[1]+1] = chessColor
			newMatrix[after[0]][after[1]-1] = chessColor
			swapchess.append([after[0],after[1]+1])
			swapchess.append([after[0],after[1]-1])
	if (after[0], after[1])==(2, 2) or (after[0], after[1]) == (3, 3) or (after[0], after[1]) == (4, 4) or (after[0], after[1]) == (4, 2) or (after[0], after[1]) == (2, 4) : 
		if (newMatrix[after[0]+1][after[1]+1] == -chessColor) and (newMatrix[after[0]-1][after[1]-1] == -chessColor) :
			newMatrix[after[0]+1][after[1]+1] = chessColor
			newMatrix[after[0]-1][after[1]-1] = chessColor
			swapchess.append([after[0]+1,after[1]+1])
			swapchess.append([after[0]-1,after[1]-1])
		if (newMatrix[after[0]-1][after[1]+1] == -chessColor) and (newMatrix[after[0]+1][after[1]-1] == -chessColor) :
			newMatrix[after[0]-1][after[1]+1] = chessColor
			newMatrix[after[0]+1][after[1]-1] = chessColor
			swapchess.append([after[0]-1,after[1]+1])
			swapchess.append([after[0]+1,after[1]-1])	

	return newMatrix,swapchess,chessColor,before,after


def theco(matrix):
	global isMax
	if isMax == True : 
		chess = -1
	else : chess = 1

	if matrix[2][2] == -chess :
		if len(checkaround(chess,2,2)) in [3,4] and len(checkaround(chess,2,2)) >=3 :
			return chess

	if matrix[3][3] == -chess :
		if len(checkaround(chess,3,3)) in [3,4] and len(checkaround(chess,3,3)) >=3 :
			return chess

	if matrix[2][4] == -chess :
		if len(checkaround(chess,2,4)) in [3,4] and len(checkaround(chess,2,4)) >=3 :
			return chess

	if matrix[4][2] == -chess :
		if len(checkaround(chess,4,2)) in [3,4] and len(checkaround(chess,4,2)) >=3 :
			return chess

	if matrix[4][4] == -chess :
		if len(checkaround(chess,4,4)) in [3,4] and len(checkaround(chess,4,4)) >=3 :
			return chess
	return 0

evaluate_matrix = [[0,0,0,0,0,0],
				[0,3,3,5,3,3],
				[0,3,8,4,8,3],
				[0,5,4,8,4,5],
				[0,3,8,4,8,3],
				[0,3,3,5,3,3]]

def get_all_value_of_matrix(matrix):
	value = 0
	for y in range(1, 6):
		for x in range(1, 6) :
			if matrix[x][y] != 0 :
				value -= (evaluate_matrix[x][y] + 20 + 5*len(possible(matrix[x][y],x,y)))*matrix[x][y]
	value += theco(matrix)
	return value

def get_all_value(matrix):
	value = 0
	for y in range(1, 6):
		for x in range(1, 6) :
				value -= matrix[x][y]
	return value

def undo(newMatrix, swapchess, chessColor, before, after):
	newMatrix[before[0]][before[1]] = chessColor
	newMatrix[after[0]][after[1]] = 0
	for i in range(len(swapchess)) :
		newMatrix[swapchess[i][0]][swapchess[i][1]] = - chessColor
	return newMatrix

def minimax(deep, newMatrix, alpha, beta, isMax):
	global time,before_move
	time += 1

	swap_move = []

	if deep == 0:
		return -get_all_value_of_matrix(newMatrix)

	all_ways = get_way(newMatrix, not isMax,before_move)

	if isMax :
		bestValue = -9999
		for i in range(len(all_ways)):
			swap_move = before_move
			before_move = all_ways[i]
			newMatrix,swapchess,chessColor,before,after = move_not_real(all_ways[i],newMatrix)
			bestValue = max(bestValue,minimax(deep - 1,newMatrix,alpha,beta,not isMax))
			newMatrix = undo(newMatrix,swapchess,chessColor,before,after)
			before_move = swap_move
			
			alpha = max(alpha,bestValue)

			if beta <= alpha :
				return bestValue
		return bestValue
	
	else :
		bestValue = 9999
		for i in range(len(all_ways)):
			swap_move = before_move
			before_move = all_ways[i]
			newMatrix,swapchess,chessColor,before,after = move_not_real(all_ways[i],newMatrix)
			bestValue = min(bestValue,minimax(deep - 1,newMatrix,alpha,beta,not isMax))
			newMatrix = undo(newMatrix,swapchess,chessColor,before,after)
			before_move = swap_move

			beta = min(beta,bestValue)

			if beta <= alpha :
				return bestValue
		return bestValue

time = 0
totaltime = 0

def getBestMove(matrix,deep,isMax):
	global time,before_move,totaltime
	time = 0
	undoMatrix = []
	swap_move = []
	all_ways = get_way(matrix, not isMax,before_move)
	bestMoveValue = -9999
	bestMove = []
	for i in range(len(all_ways)):
		swap_move = before_move
		before_move = all_ways[i]
		matrix,swapchess,chessColor,before,after = move_not_real(all_ways[i],matrix)
		value = minimax(deep - 1,matrix,-10000,10000,not isMax)
		matrix = undo(matrix,swapchess,chessColor,before,after)
		before_move = swap_move

		if value >= bestMoveValue:
			bestMoveValue = value
			bestMove = all_ways[i]

	print(time)		
	totaltime = totaltime + time
	return bestMove

############################################################## Kiem tra ket thuc game 

def termital_test():
	if get_all_value(matrix) == 16 or get_all_value(matrix) == -16  :
		return True
	elif before_move:
		if len(get_way(matrix,isMax,before_move)) == 0:
			return True
	else : return False

#####################################################################################

i_click = -1
click = [0,0]
Block_current = [0,0]
click1 = False
click2 = True
listPossibleMove = []
isCheckmate = False
p1_turn = True
p2_turn = False

def change_turn():
	global p1_turn,p2_turn
	if p1_turn :
		p1_turn = False
		p2_turn = True
	else :
		p2_turn = False
		p1_turn = True

location()
dis.fill((255,255,255))
dis.blit(map,(20,20))
xepquan()

################################################################ Vong lap game
game_over = False #Biến đánh dấu sự kiện kết thúc game
isMax = True
before_move = []

while not game_over:
	mouse = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_over = True
		elif event.type == MOUSEMOTION :
			xmouse, ymouse = event.pos

		if event.type == pygame.MOUSEBUTTONDOWN: 

			#if the mouse is clicked on the 
			# button the game is terminated 
			if 150 <= mouse[0] <= 290 and 270 <= mouse[1] <= 310: 
				matrix  = [
							[0, 0, 0, 0, 0, 0],
							[0,-1,-1,-1, 1, 1],
							[0,-1, 0, 0, 0, 1],
							[0,-1, 0, 0, 0, 1],
							[0,-1, 0, 0, 0, 1],
							[0,-1,-1, 1, 1, 1]
				]
				before_move = []
				dis.fill((255,255,255))
				dis.blit(map,(20,20))
				xepquan()

	isClick, nothing1, nothing2 = pygame.mouse.get_pressed()
	block = mouse_stay()
	
	if block != [0,0]:
		Block_current = mouse_stay()

	change = False

	if p1_turn and isClick and (12 <= xmouse <= 440) and (12 <= ymouse <= 440) :
		if click[0] == 1 or matrix[Block_current[0]][Block_current[1]] < 0:
			pygame.event.wait()
			i_click += 1;
			click[i_click%2] = 1
			click[(i_click+1) % 2] = 0
			change = True
		elif isClick:
			pygame.event.wait()
			click = [0,0]
	move()

	if termital_test():
		if num(-1)<num(1) :
			dis.blit(lose,(-30,30))
			if 150 <= mouse[0] <= 300 and 270 <= mouse[1] <= 310: 
				pygame.draw.rect(dis,color_light,[150,270,150,40]) 
			else: 
				pygame.draw.rect(dis,color_dark,[150,270,150,40])
			dis.blit(text,(150,270))
		else :
			dis.blit(win,(-30,30))
			if 150 <= mouse[0] <= 300 and 270 <= mouse[1] <= 310: 
				pygame.draw.rect(dis,color_light,[150,270,150,40]) 
			else: 
				pygame.draw.rect(dis,color_dark,[150,270,150,40])
			dis.blit(text,(150,270))	
		print(totaltime)

	if p2_turn:
		bestMove = getBestMove(matrix,4,True)
		matrix,swapchess,chessColor,before,after = move_not_real(bestMove,matrix)
		print(bestMove)
		before_move = bestMove
		dis.fill((255,255,255))
		dis.blit(map,(20,20))
		dis.blit(yellow,(column[before_move[0]],row[before_move[1]]))
		xepquan()

		change_turn()

	fpsClock.tick(FPS)
	pygame.display.update()
	
	if termital_test():
		if num(-1)<num(1) :
			dis.blit(lose,(-30,30))
			dis.blit(text,(150,270))
			if 150 <= mouse[0] <= 300 and 270 <= mouse[1] <= 310: 
				pygame.draw.rect(dis,color_light,[150,270,150,40]) 
			else: 
				pygame.draw.rect(dis,color_dark,[150,270,150,40])
		else :
			dis.blit(win,(-30,30))	
			if 150 <= mouse[0] <= 300 and 270 <= mouse[1] <= 310: 
				pygame.draw.rect(dis,color_light,[150,270,150,40]) 
			else: 
				pygame.draw.rect(dis,color_dark,[150,270,150,40])
			dis.blit(text,(150,270))
		print(totaltime)

pygame.quit()
	