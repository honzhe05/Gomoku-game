const API = "https://gomoku-game-xs81.onrender.com";

let size = 15;
document.documentElement.style.setProperty('--size', size);
const cells = [];
let player = 1;
let game_id;
let level = "";
let isThinking = false;
let change = false;

const boardDiv = document.getElementById("Board");

function check_win(winner, cnt) {
  if (!winner) {
    if (cnt >= size * size) {
      alert(`A tie! That's impossible!`);
      return true;
    }
    return false;
  }

  if (level) {
    if (winner === 1) {
      alert(`You won after ${cnt} moves!`);
    } else {
      alert(`AI won. You lose after ${cnt} moves!`);
    }
  } else {
    if (winner === 1) {
      alert(`Black won after ${cnt} moves!`);
    } else {
      alert(`White won after ${cnt} moves!`);
    }
  }

  return true;
}

async function setStone(i, j, player) {
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
        size === 15 && (
          (i === 3 && j === 3) ||
          (i === 7 && j === 7) ||
          (i === 3 && j === 11) ||
          (i === 11 && j === 3) ||
          (i === 11 && j === 11)
        ) ||
        size === 19 && (
          (i === 4 && j === 4) ||
          (i === 9 && j === 9) ||
          (i === 4 && j === 14) ||
          (i === 14 && j === 4) ||
          (i === 14 && j === 14)
        )
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

  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
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
  
  await reDraw();
}

async function placeStone(row, col) {
  if (!game_id) return;
  if (isThinking) return;
  if (player === 2 && level) return;

  const res = await fetch(`${API}/move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id, row, col, size })
  });

  const data = await res.json();

  if (!data.success) return;

  player = data.player;
  await setStone(data.row, data.col, player);
  updateTurnIndicator();
  
  if (check_win(data.winner, data.count)) {
    return;
  }
  
  if (level) {
    player = 2
    isThinking = true;
  
    setTimeout(async () => {
      await aiTurn();
      isThinking = false;
    }, 300);
  }
}

async function resetGame() {
  if (!game_id) return;
  
  createBoard();

  await fetch(`${API}/reset`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id })
  });

  player = 1
  const stone = document.getElementById("turn-stone");
  if (!stone) return;
  stone.style.background = "black";
}

async function aiTurn() {
  if (!game_id || player != 2) return;
  
  const res = await fetch(`${API}/ai_move`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ game_id, level, size })
  });
  
  const data = await res.json();
  await setStone(data.row, data.col, data.player);
  
  updateTurnIndicator();
  player = 1;
  
  check_win(data.winner, data.count);
}

function updateTurnIndicator() {
  const stone = document.getElementById("turn-stone");
  if (!stone) return;

  stone.style.background = (player === 2) ? "black" : "white";
}

async function startPlay() {
  document.getElementById("menu").classList.add("hidden");
  document.getElementById("sign").classList.remove("hidden");
  document.getElementById("playscreen").classList.remove("hidden");
  
  createBoard();
  await initGame();
  if (change) {
    await resetGame();
    change = false;
  } else {
    updateTurnIndicator();
  }
}

async function backToMain() {
  document.getElementById("menu").classList.remove("hidden");
  document.getElementById("sign").classList.add("hidden");
  document.getElementById("playscreen").classList.add("hidden");
  document.getElementById("levelmenu").classList.add("hidden")
  document.getElementById("diff").classList.add("hidden")
  
  if (level) {
    await initGame();
    await resetGame();
  }
  level = "";
}

function toSelectLevel() {
  document.getElementById("menu").classList.add("hidden")
  document.getElementById("levelmenu").classList.remove("hidden")
}

async function startAi() {
  document.getElementById("levelmenu").classList.add("hidden")
  document.getElementById("playscreen").classList.remove("hidden");
  document.getElementById("sign").classList.remove("hidden");
  
  document.getElementById("diff").textContent = `Difficulty: ${level}`
  document.getElementById("diff").classList.remove("hidden")
  
  createBoard();
  await initGame();
  await resetGame();
}

async function selectEasy() {
  level = "easy";
  await startAi();
}

async function selectNormal() {
  level = "normal";
  await startAi();
}

async function selectHard() {
  level = "hard";
  await startAi();
}

function changeSize() {
  size = (size === 19) ? 15 : 19;
  document.documentElement.style.setProperty('--size', size);
  change = true;
  
  document.getElementById("Change").textContent = `Board size: ${size}*${size}`;
}

function incom() {
  alert("How could that be? (Incomplete)");
}