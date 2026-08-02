// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let timerStart = null;
let timerInterval = null;
let currentDifficulty = 'medium';
let hintsUsed = 0;
const LEADERBOARD_KEY = 'sudoku-leaderboard';

function formatTime(seconds) {
  const mins = String(Math.floor(seconds / 60)).padStart(2, '0');
  const secs = String(seconds % 60).padStart(2, '0');
  return `${mins}:${secs}`;
}

function startTimer() {
  stopTimer();
  timerStart = Date.now();
  const timerDisplay = document.getElementById('timer');
  const updateTimer = () => {
    const elapsedSeconds = Math.floor((Date.now() - timerStart) / 1000);
    timerDisplay.innerText = `Time: ${formatTime(elapsedSeconds)}`;
  };
  updateTimer();
  timerInterval = window.setInterval(updateTimer, 1000);
}

function stopTimer() {
  if (timerInterval) {
    window.clearInterval(timerInterval);
    timerInterval = null;
  }
}

function loadLeaderboard() {
  const stored = localStorage.getItem(LEADERBOARD_KEY);
  if (!stored) return [];
  try {
    return JSON.parse(stored);
  } catch (error) {
    return [];
  }
}

function saveLeaderboard(entries) {
  localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(entries));
}

function renderLeaderboard() {
  const entries = loadLeaderboard().sort((a, b) => a.timeSeconds - b.timeSeconds);
  const tbody = document.getElementById('leaderboard-body');
  tbody.innerHTML = '';
  if (entries.length === 0) {
    const emptyRow = document.createElement('tr');
    emptyRow.innerHTML = '<td colspan="5">No scores yet</td>';
    tbody.appendChild(emptyRow);
    return;
  }
  entries.slice(0, 10).forEach((entry, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${entry.name}</td>
      <td>${formatTime(entry.timeSeconds)}</td>
      <td>${entry.difficulty}</td>
      <td>${entry.hintsUsed}</td>
    `;
    tbody.appendChild(row);
  });
}

function addScoreToLeaderboard(name, timeSeconds, difficulty, hintsUsedCount) {
  const entries = loadLeaderboard();
  entries.push({name, timeSeconds, difficulty, hintsUsed: hintsUsedCount});
  entries.sort((a, b) => a.timeSeconds - b.timeSeconds);
  const topEntries = entries.slice(0, 10);
  saveLeaderboard(topEntries);
  renderLeaderboard();
}

function applyTheme(isDark) {
  document.body.classList.toggle('dark-theme', isDark);
  localStorage.setItem('sudoku-theme', isDark ? 'dark' : 'light');
}

function getBoardValues() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return board;
}

function isCellValid(board, row, col, value) {
  if (!value) return true;
  for (let c = 0; c < SIZE; c++) {
    if (c !== col && board[row][c] === value) return false;
  }
  for (let r = 0; r < SIZE; r++) {
    if (r !== row && board[r][col] === value) return false;
  }
  const boxRow = Math.floor(row / 3) * 3;
  const boxCol = Math.floor(col / 3) * 3;
  for (let r = boxRow; r < boxRow + 3; r++) {
    for (let c = boxCol; c < boxCol + 3; c++) {
      if ((r !== row || c !== col) && board[r][c] === value) return false;
    }
  }
  return true;
}

function refreshLiveValidation() {
  const board = getBoardValues();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const inp = inputs[idx];
      if (inp.disabled) {
        inp.className = 'sudoku-cell prefilled';
        continue;
      }
      const val = inp.value;
      if (!val) {
        inp.className = 'sudoku-cell';
        continue;
      }
      const parsedValue = parseInt(val, 10);
      const isValid = isCellValid(board, i, j, parsedValue);
      inp.className = isValid ? 'sudoku-cell valid' : 'sudoku-cell invalid';
    }
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        refreshLiveValidation();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function setMessage(text, isError = false) {
  const msg = document.getElementById('message');
  msg.style.color = isError ? '#d32f2f' : '#1976d2';
  msg.innerText = text;
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
  refreshLiveValidation();
}

async function newGame() {
  currentDifficulty = document.getElementById('difficulty-select').value;
  try {
    const res = await fetch(`/new?difficulty=${encodeURIComponent(currentDifficulty)}`);
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Unable to start a new game.');
    }
    renderPuzzle(data.puzzle);
    setMessage('');
    hintsUsed = 0;
    startTimer();
  } catch (error) {
    setMessage(error.message || 'Unable to start a new game.', true);
  }
}

async function applyHint() {
  try {
    const res = await fetch('/hint');
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Unable to fetch a hint.');
    }

    const idx = data.row * SIZE + data.col;
    const boardDiv = document.getElementById('sudoku-board');
    const inputs = boardDiv.getElementsByTagName('input');
    const inp = inputs[idx];
    inp.value = data.value;
    inp.disabled = true;
    inp.className = 'sudoku-cell hint';
    puzzle[data.row][data.col] = data.value;
    hintsUsed += 1;
    setMessage(`Hint used (${hintsUsed})`);
  } catch (error) {
    setMessage(error.message || 'Unable to fetch a hint.', true);
  }
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getBoardValues();
  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || 'Unable to check the solution.');
    }

    const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
    for (let idx = 0; idx < inputs.length; idx++) {
      const inp = inputs[idx];
      if (inp.disabled) {
        if (inp.className.includes('hint')) {
          inp.className = 'sudoku-cell hint';
        } else {
          inp.className = 'sudoku-cell prefilled';
        }
        continue;
      }
      inp.className = 'sudoku-cell';
      if (incorrect.has(idx)) {
        inp.className = 'sudoku-cell incorrect';
      }
    }
    if (incorrect.size === 0) {
      stopTimer();
      const elapsedSeconds = Math.floor((Date.now() - timerStart) / 1000);
      setMessage(`Congratulations! You solved it in ${formatTime(elapsedSeconds)} on ${currentDifficulty.charAt(0).toUpperCase() + currentDifficulty.slice(1)} difficulty.`);

      const playerName = window.prompt('Enter your name for the leaderboard:', 'Player');
      if (playerName) {
        addScoreToLeaderboard(playerName.trim(), elapsedSeconds, currentDifficulty, hintsUsed);
      }
    } else {
      setMessage('Some cells are incorrect.', true);
    }
  } catch (error) {
    setMessage(error.message || 'Unable to check the solution.', true);
  }
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', applyHint);
  document.getElementById('theme-toggle').addEventListener('click', () => {
    const isDark = !document.body.classList.contains('dark-theme');
    applyTheme(isDark);
    document.getElementById('theme-toggle').innerText = isDark ? 'Switch to Light Mode' : 'Toggle Dark Mode';
  });
  const savedTheme = localStorage.getItem('sudoku-theme');
  const isDark = savedTheme === 'dark';
  applyTheme(isDark);
  document.getElementById('theme-toggle').innerText = isDark ? 'Switch to Light Mode' : 'Toggle Dark Mode';
  renderLeaderboard();
  // initialize
  newGame();
});
