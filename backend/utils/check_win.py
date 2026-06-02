def check_win(board, row, col, player):
    directions = [
        (1, 0),   # 左右
        (0, 1),   # 上下
        (1, 1),   # 斜 \
        (1, -1)   # 斜 /
    ]

    for dr, dc in directions:
        count = 1 
        
        r, c = row + dr, col + dc
        while 0 <= r < 15 and 0 <= c < 15 and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        r, c = row - dr, col - dc
        while 0 <= r < 15 and 0 <= c < 15 and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= 5:
            return True

    return False