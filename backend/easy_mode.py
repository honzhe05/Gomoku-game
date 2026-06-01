from check_win import check_win
import random

size = 15

def easy_mode(board):
    for i in range(size): # check 4-in-a-row
        for j in range(size):
            if board[i][j] != 0:
                continue

            board[i][j] = 2 # check win
            if check_win(board, i, j, 2):
                board[i][j] = 0
                return i, j
            
            board[i][j] = 1 # check lose
            if check_win(board, i, j, 1):
                board[i][j] = 0
                return i, j
                
            board[i][j] = 0

    candidates = []
    for i in range(size): # check nearby
        for j in range(size):
            if board[i][j] == 2:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                          
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < size and 0 <= nj < size:
                            if board[ni][nj] == 0:
                                candidates.append((ni, nj))
    if candidates:
        return random.choice(candidates)
            
    empty = []
    for i in range(size): # random choice
        for j in range(size):
            if board[i][j] == 0:
                empty.append((i, j))
        
    return random.choice(empty)