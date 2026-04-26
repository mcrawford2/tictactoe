const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const newGameBtn = document.getElementById("new-game");
const nameFormEl = document.getElementById("name-form");
const playerXNameInputEl = document.getElementById("player-x-name");
const playerONameInputEl = document.getElementById("player-o-name");
const cells = Array.from(document.querySelectorAll(".cell"));

let state = null;

function playerNameFor(currentState, symbol) {
	return currentState?.player_names?.[symbol] || `Player ${symbol}`;
}

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

function render(currentState) {
	state = currentState;
	statusEl.textContent = statusText(currentState);
	playerXNameInputEl.value = playerNameFor(currentState, "X");
	playerONameInputEl.value = playerNameFor(currentState, "O");

	cells.forEach((cell, index) => {
		const value = currentState.board[index];
		cell.textContent = value;
		cell.disabled = Boolean(value) || currentState.is_over;
		cell.classList.toggle("filled", Boolean(value));
	});
}

async function getState() {
	const response = await fetch("/api/state");
	const data = await response.json();
	render(data);
}

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

function currentInputNames() {
	return {
		X: playerXNameInputEl.value.trim() || "Player X",
		O: playerONameInputEl.value.trim() || "Player O",
	};
}

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

getState();
