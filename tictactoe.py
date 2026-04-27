"""Simple two-player terminal Tic-Tac-Toe game."""

WINNING_COMBINATIONS: list[tuple[int, int, int]] = [ #list[tuple[int, int, int]]: a type hint saying this is a list of 3-number tuples.
	(0, 1, 2),
	(3, 4, 5),
	(6, 7, 8),
	(0, 3, 6),
	(1, 4, 7),
	(2, 5, 8),
	(0, 4, 8),
	(2, 4, 6),
]


def draw_board(board: list[str]) -> None: #None means function doesn't return a value. Game performs actions rather than giving back data.
	"""Print the board in a 3x3 layout."""
	# Show open squares as 1-9 so players know available moves.
	display = [board[i] if board[i] != " " else str(i + 1) for i in range(9)]
	print()
	print(f" {display[0]} | {display[1]} | {display[2]}")
	print("---+---+---")
	print(f" {display[3]} | {display[4]} | {display[5]}")
	print("---+---+---")
	print(f" {display[6]} | {display[7]} | {display[8]}")
	print()


def get_move(board: list[str], player_name: str) -> int:
	"""Get a valid move from the current player."""
	while True:
		raw = input(f"{player_name}, choose a square (1-9): ").strip()

		if not raw.isdigit():
			print("Please enter a number from 1 to 9.")
			continue

		position = int(raw)
		if position < 1 or position > 9:
			print("That square is out of range. Choose 1-9.")
			continue

		index = position - 1
		if board[index] != " ":
			print("That square is already occupied. Try again.")
			continue

		return index


def check_winner(board: list[str], player: str) -> bool:
	"""Return True if the player has any winning line."""
	for a, b, c in WINNING_COMBINATIONS:
		if board[a] == board[b] == board[c] == player: #all three squares in a winning combo must belong to the same player for them to win
			return True
	return False


def check_draw(board: list[str]) -> bool:
	"""Return True if all squares are filled."""
	return " " not in board


def get_player_name(symbol: str) -> str:
	"""Prompt for a non-empty player name for the given symbol."""
	while True:
		name = input(f"Enter name for Player {symbol}: ").strip()
		if name:
			return name
		print("Name cannot be empty.")


def ask_play_again(player_x_name: str, player_o_name: str) -> None:
	"""Prompt to start another game and handle replays."""
	while True:
		answer = input("Play again? (y/n): ").strip().lower()
		if answer in ("y", "yes"):
			# Reuse player names so rematches start quickly.
			main(player_x_name, player_o_name)
			return
		if answer in ("n", "no"):
			print("Thanks for playing!")
			return
		print("Please enter 'y' or 'n'.")


def main(player_x_name: str | None = None, player_o_name: str | None = None) -> None: #defines main with player names, program asks for names if they aren't already provided
	"""Runs one game, then optionally starts a rematch."""
	board = [" "] * 9
	current_player = "X"
	if player_x_name is None:
		player_x_name = get_player_name("X")
	if player_o_name is None:
		player_o_name = get_player_name("O")
	player_names = {"X": player_x_name, "O": player_o_name}

	print("Welcome to Tic-Tac-Toe!")

	while True:
		draw_board(board)
		move = get_move(board, player_names[current_player])
		board[move] = current_player

		if check_winner(board, current_player):
			draw_board(board)
			print(f"{player_names[current_player]} ({current_player}) wins!")
			break

		if check_draw(board):
			draw_board(board)
			print("It's a draw!")
			break

		# Alternate turn between X and O.
		current_player = "O" if current_player == "X" else "X"

	ask_play_again(player_x_name, player_o_name)


if __name__ == "__main__":
	main()
