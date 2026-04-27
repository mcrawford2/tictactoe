/**DOM elements */ 
const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const newGameBtn = document.getElementById("new-game");
const nameFormEl = document.getElementById("name-form");
const playerXNameInputEl = document.getElementById("player-x-name");
const playerONameInputEl = document.getElementById("player-o-name");
const cells = Array.from(document.querySelectorAll(".cell"));

// Snapshot of the latest server state used by render and click handlers.
let state = null;

/**
 * Resolve a display name for a symbol (X/O), with a safe fallback.
 */
function playerNameFor(currentState, symbol) {
	return currentState?.player_names?.[symbol] || `Player ${symbol}`;
}

/**
 * Build the status message shown above the board.
 */
function statusText(currentState) {
	if (!currentState) {
		return "Loading game...";
	}

	if (currentState.winner) {
		const winnerName = playerNameFor(currentState, currentState.winner);
		return `${winnerName} (${currentState.winner}) wins!`;
	}

	if (currentState.is_draw) {
		return "Draw game.";
	}

	const currentName = playerNameFor(currentState, currentState.current_player);
	return `${currentName}'s turn (${currentState.current_player})`;
}

/**
 * Render the full UI from the latest game state object.
 */
function render(currentState) {
	state = currentState;
	statusEl.textContent = statusText(currentState);
	playerXNameInputEl.value = playerNameFor(currentState, "X");
	playerONameInputEl.value = playerNameFor(currentState, "O");

	cells.forEach((cell, index) => {
		const value = currentState.board[index];
		cell.textContent = value;
		// Disable filled cells and all cells once the game is over.
		cell.disabled = Boolean(value) || currentState.is_over;
		cell.classList.toggle("filled", Boolean(value));
	});
}

/**
 * Load the current game state from the backend.
 */
async function getState() {
	const response = await fetch("/api/state");
	const data = await response.json();
	render(data);
}

/**
 * Submit a move for a board position, then re-render from server response.
 */
async function makeMove(position) {
	const response = await fetch("/api/move", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ position }),
	});

	const data = await response.json();
	if (!response.ok) {
		statusEl.textContent = data.error || "Move failed.";
		if (data.state) {
			render(data.state);
		}
		return;
	}

	render(data);
}

/**
 * Read and normalize player names from the form.
 */
function currentInputNames() {
	return {
		X: playerXNameInputEl.value.trim() || "Player X",
		O: playerONameInputEl.value.trim() || "Player O",
	};
}

/**
 * Persist player names on the backend.
 */
async function setPlayerNames() {
	const response = await fetch("/api/player-names", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ player_names: currentInputNames() }),
	});

	const data = await response.json();
	if (!response.ok) {
		statusEl.textContent = data.error || "Failed to set player names.";
		return;
	}

	render(data);
}

/**
 * Start a fresh game while keeping current player names.
 */
async function newGame() {
	const response = await fetch("/api/new-game", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ player_names: currentInputNames() }),
	});
	const data = await response.json();
	render(data);
}

// Event delegation: one board listener handles clicks for all cells.
boardEl.addEventListener("click", (event) => {
	const cell = event.target.closest(".cell");
	if (!cell || !state) {
		return;
	}

	const position = Number(cell.dataset.position);
	makeMove(position);
});

newGameBtn.addEventListener("click", () => {
	newGame();
});

nameFormEl.addEventListener("submit", (event) => {
	event.preventDefault();
	setPlayerNames();
});

// Initial page load sync.
getState();
