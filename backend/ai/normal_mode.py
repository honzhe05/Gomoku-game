import random
from utils.check_win import check_win

size = 15
dirs = [
    (1,0),   # |
    (0,1),   # —
    (1,1),   # \
    (1,-1)   # /
]

def count_score(cnt):
    if cnt >= 5:
        return 10000
    if cnt == 4:
        return 1000
    if cnt == 3:
        return 100
    if cnt == 2:
        return 10
    return 0

def line_info(board, i, j, dx, dy, p):
    cnt = 1

    x, y = i + dx, j + dy
    while 0 <= x < size and 0 <= y < size and board[x][y] == p:
        cnt += 1
        x += dx
        y += dy

    x, y = i - dx, j - dy
    while 0 <= x < size and 0 <= y < size and board[x][y] == p:
        cnt += 1
        x -= dx
        y -= dy

    return count_score(cnt)

def normal_mode(board):
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
          
    score = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                board[i][j] = 2
                attack = 0
                for nx, ny in dirs:
                    attack += line_info(board, i, j, nx, ny, 2) * 0.5
                    
                board[i][j] = 1
                defense = 0
                for nx, ny in dirs:
                    defense += line_info(board, i, j, nx, ny, 1)
                    
                board[i][j] = 0
                
                score[i][j] = attack + defense
     
    empty = []
    for i in range(size): # random choice
        for j in range(size):
            if board[i][j] == 0:
                empty.append((i, j))
     
    t = random.randint(0, 10)
    max_list = []
    if t not in [0, 1]:
        maxi = 0
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
        return random.choice(empty)
    else:
        return random.choice(empty)