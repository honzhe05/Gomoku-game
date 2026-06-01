from check_win import check_win
import random

size = 15

def easy_mode(board):
    stone_count = 0
    for row in board:
        for cell in row:
            if cell != 0:
                stone_count += 1

    if stone_count == 0:
        return random.choice([
            (7, 7), (7, 6), (7, 8),
            (6, 7), (8, 7)
        ])
        
    for i in range(size): # check win
        for j in range(size):
            if board[i][j] != 0:
                continue

            board[i][j] = 2
            if check_win(board, i, j, 2):
                board[i][j] = 0
                return i, j

            board[i][j] = 0

    for i in range(size): # check lose
        for j in range(size):
            if board[i][j] != 0:
                continue

            board[i][j] = 1
            if check_win(board, i, j, 1):
                board[i][j] = 0
                return i, j

            board[i][j] = 0
            
    empty = []
    for i in range(size): # random
        for j in range(size):
            if board[i][j] == 0:
                empty.append((i, j))
        
    return random.choice(empty)