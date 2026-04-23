WINNING_COMBINATIONS = [
	(0, 1, 2),
	(3, 4, 5),
	(6, 7, 8),
	(0, 3, 6),
	(1, 4, 7),
	(2, 5, 8),
	(0, 4, 8),
	(2, 4, 6),
]


def draw_board(board):
	"""Print the board in a 3x3 layout."""
	display = [board[i] if board[i] != " " else str(i + 1) for i in range(9)]
	print()
	print(f" {display[0]} | {display[1]} | {display[2]}")
	print("---+---+---")
	print(f" {display[3]} | {display[4]} | {display[5]}")
	print("---+---+---")
	print(f" {display[6]} | {display[7]} | {display[8]}")
	print()


def get_move(board, player):
	"""Get a valid move from the current player."""
	while True:
		raw = input(f"Player {player}, choose a square (1-9): ").strip()

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


def check_winner(board, player):
	"""Return True if the player has any winning line."""
	for a, b, c in WINNING_COMBINATIONS:
		if board[a] == board[b] == board[c] == player:
			return True
	return False


def check_draw(board):
	"""Return True if all squares are filled."""
	return " " not in board


def main():
	board = [" "] * 9
	current_player = "X"

	print("Welcome to Tic-Tac-Toe!")

	while True:
		draw_board(board)
		move = get_move(board, current_player)
		board[move] = current_player

		if check_winner(board, current_player):
			draw_board(board)
			print(f"Player {current_player} wins!")
			break

		if check_draw(board):
			draw_board(board)
			print("It's a draw!")
			break

		current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
	main()
