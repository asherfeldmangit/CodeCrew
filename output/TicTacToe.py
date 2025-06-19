import random

class T3Game:
    def __init__(self, game_mode: str = "PvC") -> None:
        """
        Initialize the Tic Tac Toe game.

        Parameters:
            game_mode (str): "PvC" for player vs computer, "PvP" for two-player game.
        """
        self.game_mode = game_mode
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]

    def reset_board(self) -> None:
        """
        Resets the game board to the initial empty state.
        """
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def display_board(self) -> None:
        """
        Displays the current state of the game board.
        """
        for row in self.board:
            print('|'.join(cell if cell else ' ' for cell in row))
            print('-' * 5)

    def make_move(self, row: int, col: int) -> bool:
        """
        Attempts to place the current player's mark on the board.

        Parameters:
            row (int): The row index (0-2).
            col (int): The column index (0-2).

        Returns:
            bool: True if move was successful, False if the cell is already occupied.
        """
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '':
            self.board[row][col] = self.current_player
            return True
        return False

    def check_win(self) -> bool:
        """
        Checks if the current state of the board has a winner.

        Returns:
            bool: True if the current player has won, False otherwise.
        """
        b = self.board
        # Check rows and columns
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != '':
                return True
            if b[0][i] == b[1][i] == b[2][i] != '':
                return True
        # Check diagonals
        if b[0][0] == b[1][1] == b[2][2] != '':
            return True
        if b[0][2] == b[1][1] == b[2][0] != '':
            return True
        return False

    def check_draw(self) -> bool:
        """
        Checks if the game is a draw.

        Returns:
            bool: True if all cells are filled and no winner is found, False otherwise.
        """
        for row in self.board:
            if '' in row:
                return False
        return True

    def switch_player(self) -> None:
        """
        Switches the current player mark.
        """
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_available_moves(self) -> list:
        """
        Retrieves all currently empty cells as potential moves.

        Returns:
            list: A list of tuples indicating available (row, col) positions.
        """
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '':
                    moves.append((i, j))
        return moves

    def machine_move(self) -> bool:
        """
        Executes a move for the machine (computer player) in PvC mode using a simple heuristic.

        Returns:
            bool: True if a move was made, or False if no move is available.
        """
        moves = self.get_available_moves()
        if not moves:
            return False
        row, col = random.choice(moves)
        self.make_move(row, col)
        return True

    def play_turn(self, row: int = None, col: int = None) -> dict:
        """
        Processes a single turn in the game. For PvC mode, if it is the machine's turn, automatically make a machine move.

        Parameters:
            row (int): The row for the human move (ignored if machine's turn in PvC mode).
            col (int): The column for the human move.

        Returns:
            dict: A dictionary containing:
                - "board": Current state of the board.
                - "status": Message indicating if the move was successful or if the game is won/drawn.
                - "move_made": True if move was executed, False otherwise.
        """
        result = {"board": self.board, "move_made": False, "status": ""}

        # In PvC mode, if it's computer's turn, automatically move.
        if self.game_mode == "PvC" and self.current_player == 'O':
            moved = self.machine_move()
            result["move_made"] = moved
        else:
            if row is None or col is None:
                result["status"] = "Invalid move parameters for human player."
                return result
            moved = self.make_move(row, col)
            result["move_made"] = moved
            if not moved:
                result["status"] = "Invalid move, cell already taken."
                return result

        # Check game outcomes after move
        if self.check_win():
            result["status"] = f"Player {self.current_player} wins!"
        elif self.check_draw():
            result["status"] = "The game is a draw."
        else:
            self.switch_player()
            result["status"] = "Move accepted, game continues."

        result["board"] = self.board
        return result

def run_game() -> None:
    """
    Runs an interactive text-based Tic Tac Toe game using the T3Game class.

    This function prompts the user to select the game mode, then loops over user input,
    updating and displaying the board after each move until a win or draw condition is reached.
    """
    print("Welcome to Tic Tac Toe!")
    mode = input("Select game mode (PvC for Player vs Computer, PvP for Player vs Player): ").strip()
    if mode not in ["PvC", "PvP"]:
        print("Invalid mode! Defaulting to Player vs Computer.")
        mode = "PvC"

    game = T3Game(game_mode=mode)

    while True:
        game.display_board()
        # Human move if PvP mode or if it's human's turn in PvC mode (when current player is 'X')
        if mode == "PvP" or game.current_player == 'X':
            try:
                user_input = input(f"Player {game.current_player}, enter your move as 'row col': ")
                row, col = map(int, user_input.split())
            except ValueError:
                print("Invalid input format. Please enter two numbers separated by a space (e.g., 0 1).")
                continue
            result = game.play_turn(row, col)
        else:
            print("Computer's turn.")
            result = game.play_turn()

        print(result["status"])
        if "wins" in result["status"] or "draw" in result["status"]:
            game.display_board()
            print("Game Over.")
            break

if __name__ == "__main__":
    run_game()