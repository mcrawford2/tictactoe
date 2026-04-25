from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def _new_game_state() -> dict:
	return {
		"board": ["" for _ in range(9)],
		"current_player": "X",
		"winner": None,
		"is_draw": False,
		"is_over": False,
	}


game_state = _new_game_state()


def _calculate_winner(board: list[str]) -> str | None:
	winning_lines = [
		(0, 1, 2),
		(3, 4, 5),
		(6, 7, 8),
		(0, 3, 6),
		(1, 4, 7),
		(2, 5, 8),
		(0, 4, 8),
		(2, 4, 6),
	]

	for a, b, c in winning_lines:
		if board[a] and board[a] == board[b] == board[c]:
			return board[a]

	return None


@app.route("/")
def home() -> str:
	return render_template("index.html")


@app.get("/api/state")
def get_state() -> dict:
	return jsonify(game_state)


@app.post("/api/new-game")
def new_game() -> dict:
	global game_state
	game_state = _new_game_state()
	return jsonify(game_state)


@app.post("/api/move")
def make_move() -> tuple[dict, int] | dict:
	data = request.get_json(silent=True) or {}
	position = data.get("position")

	if not isinstance(position, int) or not 0 <= position <= 8:
		return jsonify({"error": "Position must be an integer from 0 to 8."}), 400

	if game_state["is_over"]:
		return jsonify({"error": "Game is already over.", "state": game_state}), 400

	if game_state["board"][position]:
		return jsonify({"error": "Cell is already taken.", "state": game_state}), 400

	game_state["board"][position] = game_state["current_player"]

	winner = _calculate_winner(game_state["board"])
	if winner:
		game_state["winner"] = winner
		game_state["is_over"] = True
		return jsonify(game_state)

	if all(cell for cell in game_state["board"]):
		game_state["is_draw"] = True
		game_state["is_over"] = True
		return jsonify(game_state)

	game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
	return jsonify(game_state)


if __name__ == "__main__":
	app.run(debug=True)
