const API = "https://gomoku-game-xs81.onrender.com";

const size = 15;
const cells = [];
let player = 1;
let game_id;

const boardDiv = document.getElementById("Board");

function setStone(i, j, player) {
  const cell = cells[i][j];

  if (cell.dataset.filled === "1") return;

  const stone = document.createElement("div");
  stone.className = "stone " + (player === 1 ? "black" : "white");

  cell.appendChild(stone);
  cell.dataset.filled = "1";
}

function createBoard() {
  boardDiv.innerHTML = "";

  for (let i = 0; i < size; i++) {
    cells[i] = [];

    for (let j = 0; j < size; j++) {
      const cell = document.createElement("div");
      cell.className = "cell";
      
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

  for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
      if (data.board[i][j] !== 0 && !cells[i][j].dataset.filled) {
        setStone(i, j, data.board[i][j]);
      }
    }
  }
}

async function initGame() {
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
  player = data.player;

  reDraw();
}

async function placeStone(row, col) {
  if (!game_id) return;

  const res = await fetch(`${API}/move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id, row, col })
  });

  const data = await res.json();

  if (!data.success) return;

  setStone(data.row, data.col, data.player);
  
  player = data.player;
  updateTurnIndicator();

  if (data.winner) {
    alert(data.winner === 1 ? "black win" : "white win");
  }
}

async function resetGame() {
  if (!game_id) return;

  await fetch(`${API}/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id })
  });

  player = 2
  createBoard();
  updateTurnIndicator();
}

function updateTurnIndicator() {
  const stone = document.getElementById("turn-stone");
  if (!stone) return;

  stone.style.background = (player === 2) ? "black" : "white";
}

async function startTwoPlayer() {
  document.getElementById("menu").classList.add("hidden");
  document.getElementById("sign").classList.remove("hidden");
  document.getElementById("playscreen").classList.remove("hidden");
  
  createBoard();
  await initGame();
  updateTurnIndicator();
}

function backToMain() {
  document.getElementById("menu").classList.remove("hidden");
  document.getElementById("sign").classList.add("hidden");
  document.getElementById("playscreen").classList.add("hidden");
}

function vsAi() {
  alert("How could that be? (Incomplete)");
}