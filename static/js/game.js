const boardEl = document.getElementById("board");
const statusEl = document.getElementById("status");
const newGameBtn = document.getElementById("new-game");
const cells = Array.from(document.querySelectorAll(".cell"));

let state = null;

function statusText(currentState) {
	if (!currentState) {
		return "Loading game...";
	}

	if (currentState.winner) {
		return `Player ${currentState.winner} wins!`;
	}

	if (currentState.is_draw) {
		return "Draw game.";
	}

	return `Player ${currentState.current_player}'s turn`;
}

function render(currentState) {
	state = currentState;
	statusEl.textContent = statusText(currentState);

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

async function newGame() {
	const response = await fetch("/api/new-game", {
		method: "POST",
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

getState();
