import random
from check_win import check_win

size = 15
score_map = {
    (5, True, True): 10000000,
    (4, True, True): 1000000,
    (4, True, False): 100000,
    (3, True, True): 10000,
    (3, True, False): 1000,
    (2, True, True): 100,
}
dirs = [
    (1,0),   # |
    (0,1),   # —
    (1,1),   # \
    (1,-1)   # /
]

def line_info(board, i, j, dx, dy, p):
    line = []

    x, y = i - dx, j - dy
    while 0 <= x < size and 0 <= y < size:
        line.append(board[x][y])
        x -= dx
        y -= dy
    line.reverse()

    line.append(board[i][j])

    x, y = i + dx, j + dy
    while 0 <= x < size and 0 <= y < size:
        line.append(board[x][y])
        x += dx
        y += dy

    s = ''.join(str(x) for x in line)
    return s

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
          
    score = [[0]*15 for _ in range(15)]
    for i in range(size):
        for j in range(size):
            center = 14 - abs(i-7) - abs(j-7)
            score[i][j] += (center * 200)
            
            if board[i][j] == 0:
                board[i][j] = 2
                attack = 0
                for nx, ny in dirs:
                    t = line_info(board, i, j, nx, ny, 2)
                    attack += score_map[t]
                    
                board[i][j] = 1
                defense = 0
                for nx, ny in dirs:
                    t = line_info(board, i, j, nx, ny, 1)
                    defense += score_map[t]
                    
                board[i][j] = 0
                
                if defense >= 100000:
                    defense *= 3
                elif defense >= 10000:
                    defense *= 2
                score[i][j] = attack + defense
                    
    maxi, pos = 0, (-1, -1)
    for i in range(size):
        for j in range(size):
            if score[i][j] > maxi:
                maxi = score[i][j]
                pos = (i, j)
                
    if pos != (-1, -1):
        return pos
        
    empty = []
    for i in range(size): # random choice
        for j in range(size):
            if board[i][j] == 0:
                empty.append((i, j))
        
    return random.choice(empty)