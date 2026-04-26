from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def _sanitize_player_name(value: object, default_name: str) -> str:
	if isinstance(value, str):
		name = value.strip()
		if name:
			return name
	return default_name


def _player_names_from_payload(payload: dict | None = None) -> dict[str, str]:
	payload = payload or {}
	return {
		"X": _sanitize_player_name(payload.get("X"), "Player X"),
		"O": _sanitize_player_name(payload.get("O"), "Player O"),
	}


def _new_game_state(player_names: dict | None = None) -> dict:
	return {
		"board": ["" for _ in range(9)],
		"current_player": "X",
		"player_names": _player_names_from_payload(player_names),
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
	data = request.get_json(silent=True) or {}
	game_state = _new_game_state(data.get("player_names"))
	return jsonify(game_state)


@app.post("/api/player-names")
def set_player_names() -> dict:
	data = request.get_json(silent=True) or {}
	player_names = data.get("player_names")

	if not isinstance(player_names, dict):
		return jsonify({"error": "player_names must be an object with X and O."}), 400

	game_state["player_names"] = _player_names_from_payload(player_names)
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
