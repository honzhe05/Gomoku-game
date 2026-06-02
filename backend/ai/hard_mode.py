import random
from utils.check_win import check_win

size = 15
dirs = [
    (1,0),   # |
    (0,1),   # —
    (1,1),   # \
    (1,-1)   # /
]

def count_score(cnt, open1, open2):
    if cnt >= 5:
        return 1000000
    if cnt == 4 and open1 and open2:
        return 100000
    if cnt == 4:
        return 10000
    if cnt == 3 and open1 and open2:
        return 5000
    if cnt == 3:
        return 1000
    if cnt == 2:
        return 100
    return 1

def line_info(board, i, j, dx, dy, p):
    cnt = 1

    x, y = i + dx, j + dy
    open1 = False
    while 0 <= x < size and 0 <= y < size and board[x][y] == p:
        cnt += 1
        x += dx
        y += dy
    if 0 <= x < size and 0 <= y < size and board[x][y] == 0:
        open1 = True

    x, y = i - dx, j - dy
    open2 = False
    while 0 <= x < size and 0 <= y < size and board[x][y] == p:
        cnt += 1
        x -= dx
        y -= dy
    if 0 <= x < size and 0 <= y < size and board[x][y] == 0:
        open2 = True

    return count_score(cnt, open1, open2)

def hard_mode(board):
    for i in range(size):
        for j in range(size):
            if board[i][j] != 0:
                continue
    
            board[i][j] = 2
            if check_win(board, i, j, 2):
                board[i][j] = 0
                return i, j
            board[i][j] = 1
            if check_win(board, i, j, 1):
                board[i][j] = 0
                return i, j
            board[i][j] = 0
          
    score = [[0]*15 for _ in range(15)]
    for i in range(size):
        for j in range(size):
            center = 14 - abs(i-7) - abs(j-7)
            score[i][j] += (center * 50)
            
            if board[i][j] == 0:
                board[i][j] = 2
                attack = 0
                for nx, ny in dirs:
                    attack += line_info(board, i, j, nx, ny, 2)
                    
                board[i][j] = 1
                defense = 0
                for nx, ny in dirs:
                    defense += line_info(board, i, j, nx, ny, 1)
                    
                board[i][j] = 0
                
                defense *= 1.5 + (defense / 1000000)
                score[i][j] = attack + defense
                    
    maxi = 0
    max_list = []
    for i in range(size): # select maxscore
        for j in range(size):
            if board[i][j] == 0:
                if score[i][j] > maxi:
                    maxi = score[i][j]
                    max_list = []
                    max_list.append((i, j))
                elif score[i][j] == maxi:
                    max_list.append((i, j))
                    
    if max_list:
        return random.choice(max_list)
        
    empty = []
    for i in range(size): # random choice
        for j in range(size):
            if board[i][j] == 0:
                empty.append((i, j))
        
    return random.choice(empty)