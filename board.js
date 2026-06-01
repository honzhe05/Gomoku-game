const API =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:5000"
    : "https://gomoku-game-xs81.onrender.com";

const size = 15;
let board = [];
const cells = [];
let player = 1;
let game_id;

const boardDiv = document.getElementById("Board");

function renderBoard(board) {
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      const cell = cells[i][j];
      cell.innerHTML = "";

      if (
        (i === 3 && j === 3) ||
        (i === 7 && j === 7) ||
        (i === 3 && j === 11) ||
        (i === 11 && j === 3) ||
        (i === 11 && j === 11)
      ) {
        const dot = document.createElement("div");
        dot.className = "star-point";
        cell.appendChild(dot);
      }

      if (board[i][j] !== 0) {
        const stone = document.createElement("div");
        stone.className =
          "stone " + (board[i][j] === 1 ? "black" : "white");

        cell.appendChild(stone);
      }
    }
  }
}

function createBoard() {
  boardDiv.innerHTML = "";

  for (let i = 0; i < size; i++) {
    board[i] = [];
    cells[i] = [];

    for (let j = 0; j < size; j++) {
      board[i][j] = 0;

      const cell = document.createElement("div");
      cell.className = "cell";

      if (i === 0) cell.classList.add("top");
      if (i === size - 1) cell.classList.add("bottom");
      if (j === 0) cell.classList.add("left");
      if (j === size - 1) cell.classList.add("right");

      cell.onclick = () => placeStone(i, j);

      boardDiv.appendChild(cell);
      cells[i][j] = cell;
    }
  }
}

async function reDraw() {
  if (!game_id) return;
  
  const res = await fetch(`${API}/state`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id })
  });

  const data = await res.json();
  board = data.board;

  renderBoard(board);
}

window.onload = async () => {
  createBoard();

  if (!localStorage.uuid) {
    localStorage.uuid = crypto.randomUUID();
  }

  const res = await fetch(`${API}/get_game`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ uuid: localStorage.uuid })
  });

  const data = await res.json();
  game_id = data.game_id;

  reDraw();
};

async function placeStone(row, col) {
  if (!game_id) return;
  
  const res = await fetch(`${API}/move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      game_id,
      row,
      col
    })
  });

  const data = await res.json();

  if (data.success) {
    player = data.player;
    reDraw();
    
    if (data.winner) {
      win = (data.winner == 1) ? "black": "white";
      alert("winner: " + win);
      return;
    }
  }
}

async function resetGame() {
  if (!game_id) return;
  
  await fetch(`${API}/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id })
  });

  player = 1;
  await reDraw();
}