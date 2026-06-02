from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from init_db import init_db
from ai.easy_mode import easy_mode
from ai.normal_mode import normal_mode
from ai.hard_mode import hard_mode
from utils.check_win import check_win

init_db()

app = Flask(__name__)
CORS(app)

board = [[0] * 15 for _ in range(15)]
player = 1
move_count = 0
game_id = 1

def get_db():
    conn = sqlite3.connect("gomoku.db")
    conn.row_factory = sqlite3.Row
    return conn
    
def get_board(game_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT row,col,player
        FROM moves
        WHERE game_id=?
    """, (game_id,))

    moves = cur.fetchall()

    board = [[0]*15 for _ in range(15)]
    for r,c,p in moves:
        board[r][c] = p

    return board

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    game_id = data["game_id"]
    row = data["row"]
    col = data["col"]

    conn = get_db()
    cur = conn.cursor()

    # check finished
    cur.execute("SELECT status FROM games WHERE id=?", (game_id,))
    status = cur.fetchone()[0]

    if status == "finished":
        return jsonify({ "success": False, "msg": "finished" })

    # check duplicate
    cur.execute("""
        SELECT 1 FROM moves
        WHERE game_id=? AND row=? AND col=?
    """, (game_id, row, col))

    if cur.fetchone():
        return jsonify({ "success": False })

    cur.execute("SELECT COUNT(*) FROM moves WHERE game_id = ?", (game_id,))
    count = cur.fetchone()[0]
    player = 1 if count % 2 == 0 else 2

    cur.execute("""
        INSERT INTO moves (game_id,row,col,player,move_num)
        VALUES (?,?,?,?,?)
    """, (game_id, row, col, player, count + 1))
    
    board = get_board(game_id)

    winner = None
    if check_win(board, row, col, player):
        winner = player
        cur.execute("UPDATE games SET status='finished' WHERE id=?", (game_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "row": row,
        "col": col,
        "player": player,
        "winner": winner,
        "count": count + 1
    })
    
@app.route("/state", methods=["POST"])
def state():
    data = request.json
    game_id = data["game_id"]
    return jsonify({ "board": get_board(game_id) })
    
@app.route("/get_game", methods=["POST"])
def get_game():
    data = request.json
    uuid = data["uuid"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id FROM games
        WHERE player_uuid = ? AND status = 'playing'
    """, (uuid,))

    game = cur.fetchone()

    if game:
        game_id = game["id"]
    else:
        cur.execute("""
            INSERT INTO games (player_uuid, status)
            VALUES (?, 'playing')
        """, (uuid,))
        game_id = cur.lastrowid
        conn.commit()
        
    cur.execute("""
        SELECT COUNT(*) FROM moves
        WHERE game_id = ?
    """, (game_id,))
    
    count = cur.fetchone()[0]
    
    next_player = 2 if count % 2 == 0 else 1
    
    conn.close()
    
    return jsonify({
        "game_id": game_id,
        "player": next_player
    })

@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    game_id = data["game_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM moves
        WHERE game_id = ?
    """, (game_id,))

    cur.execute("""
        UPDATE games
        SET status = 'playing'
        WHERE id = ?
    """, (game_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True
    })
    
@app.route("/ai_move", methods=["POST"])
def ai_move():
    data = request.json
    level = data["level"]
    game_id = data["game_id"]

    conn = get_db()
    cur = conn.cursor()

    board = get_board(game_id)

    # choose AI move
    if level == "easy":
        row, col = easy_mode(board)
    elif level == "normal":
        row, col = normal_mode(board)
    elif level == "hard":
        row, col = hard_mode(board)
    else:
        return

    player = 2

    # get move count
    cur.execute("""
        SELECT COUNT(*) FROM moves WHERE game_id=?
    """, (game_id,))
    count = cur.fetchone()[0]

    # insert AI move
    cur.execute("""
        INSERT INTO moves (game_id, row, col, player, move_num)
        VALUES (?, ?, ?, ?, ?)
    """, (game_id, row, col, player, count + 1))

    # rebuild board after move (optional but clean)
    board = get_board(game_id)

    winner = None
    if check_win(board, row, col, player):
        winner = player
        cur.execute("""
            UPDATE games SET status='finished'
            WHERE id=?
        """, (game_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "row": row,
        "col": col,
        "player": player,
        "winner": winner
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)