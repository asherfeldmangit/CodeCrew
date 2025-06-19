```markdown
# Tic Tac Toe Game Module Design

This module is a self-contained Python module implementing the classic game Tic Tac Toe. The game supports two modes:
1. Single Player: One human player versus the machine.
2. Two Player: Two human players playing against each other.

The module defines a main class "TicTacToeGame" that encapsulates game state and logic. A helper module-level function is provided to run the game loop from a simple command line interface for testing or UI integration.

---

## Module Structure

### Class: TicTacToeGame
This class is responsible for managing the game state (i.e., the board and the current player's turn), processing moves, checking for wins/draws, and for switching between players. It also provides the machine’s move logic.

#### Attributes:
- `board`: A list of lists (3x3) representing the board, initialized to empty strings.
- `current_player`: A string that holds the symbol ('X' or 'O') of the current player.
- `game_mode`: A string indicating the mode of the game. Allowed values are `"PvC"` for Player versus Computer, and `"PvP"` for Player versus Player.

#### Methods:
- `__init__(self, game_mode: str = "PvC") -> None`  
  Initializes a new game with a 3x3 board, sets the game mode, and sets the starting player (typically 'X').  
  *Parameters:*  
    - `game_mode`: The game mode to use; default is `"PvC"`.

- `reset_board(self) -> None`  
  Resets the board to its initial empty state.

- `display_board(self) -> None`  
  Displays the current board state. This method can be used during testing or by a simple UI to show the board to the players.

- `make_move(self, row: int, col: int) -> bool`  
  Attempts to place the current player's symbol at the specified row and column.  
  *Parameters:*  
    - `row`: The board row (0-indexed).
    - `col`: The board column (0-indexed).  
  *Returns:*  
    - `True` if the move was valid and made, `False` otherwise.

- `check_win(self) -> bool`  
  Checks whether the current board state results in a win for any player.  
  *Returns:*  
    - `True` if the current player wins, `False` otherwise.

- `check_draw(self) -> bool`  
  Determines if the game is a draw (i.e., all cells are filled and no win condition is met).  
  *Returns:*  
    - `True` if the game is a draw, `False` otherwise.

- `switch_player(self) -> None`  
  Switches the current player. For example, changes from 'X' to 'O' and vice versa.

- `get_available_moves(self) -> list`  
  Returns a list of tuples representing the available moves in the board.  
  *Returns:*  
    - List of `(row, col)` tuples for every empty cell.

- `machine_move(self) -> bool`  
  Selects and makes a move for the machine when in `"PvC"` mode. The implementation can use a simple heuristic (random selection from available moves).  
  *Returns:*  
    - `True` if a machine move was made, `False` if no move is possible.

- `play_turn(self, row: int = None, col: int = None) -> dict`  
  Executes a turn by performing a human move or, when it is the machine’s turn in `"PvC"`, automatically selects a move.  
  *Parameters:*  
    - `row, col`: For human moves (ignored if current turn is for the computer in `"PvC"` mode).
  *Returns:*  
    - A dictionary containing the new board state, an indicator if the move was successful, and status messages (e.g., win, draw).

### Function: run_game()
This module-level function provides a simple loop-based user interface for testing or integration with a basic UI. It prompts users for input, displays the game board after each move, and handles win/draw announcements. This function uses an instance of TicTacToeGame.

#### Function Signature:
- `run_game() -> None`  
  Starts an interactive session of the Tic Tac Toe game.

---

## Overall Flow
1. When the module is executed as a script, it will call `run_game()`.
2. The game is initialized using an instance of `TicTacToeGame` in the desired mode (Player vs Computer or Player vs Player).
3. The board is displayed, and the game loop takes user input for moves.
4. After each move, a check is performed for a win or draw.  
5. If in `"PvC"` mode and it is the machine's turn, `machine_move()` is automatically executed.
6. The loop continues until a win or draw condition is detected.

---

## Example Outline of the Module Code

```python
import random

class TicTacToeGame:
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
        Prints the current state of the game board.
        """
        for row in self.board:
            print('|'.join(cell if cell else ' ' for cell in row))
            print("-" * 5)
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Attempts to place the current player's mark on the board.
        
        Parameters:
            row (int): The row index (0-2).
            col (int): The column index (0-2).
            
        Returns:
            bool: True if move was successful, False if the cell is already occupied.
        """
        if self.board[row][col] == '':
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
            row (int): The row for the human move.
            col (int): The column for the human move.
            
        Returns:
            dict: A dictionary containing:
                - "board": Current state of the board.
                - "status": Message indicating if the move was successful or if the game is won/drawn.
                - "move_made": True if move was executed, False otherwise.
        """
        result = {"board": self.board, "move_made": False, "status": ""}
        
        # If PvC and current player is computer, no arguments should be used.
        if self.game_mode == "PvC" and self.current_player == 'O':
            moved = self.machine_move()
            result["move_made"] = moved
        else:
            # Human move: row and col must be provided.
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
    Runs an interactive text-based Tic Tac Toe game using the TicTacToeGame class.

    This function prompts the user to select the game mode, then loops over user input,
    updating and displaying the board after each move until a win or draw.
    """
    print("Welcome to Tic Tac Toe!")
    mode = input("Select game mode (PvC for Player vs Computer, PvP for Player vs Player): ").strip()
    if mode not in ["PvC", "PvP"]:
        print("Invalid mode! Defaulting to Player vs Computer.")
        mode = "PvC"
    
    game = TicTacToeGame(game_mode=mode)
    
    while True:
        game.display_board()
        # Only ask input if it's the human player's turn (for PvC mode, computer might auto play)
        if mode == "PvP" or game.current_player == 'X':
            try:
                user_input = input(f"Player {game.current_player}, enter your move as 'row col': ")
                row, col = map(int, user_input.split())
            except ValueError:
                print("Invalid input format. Please enter two numbers separated by space (e.g., 0 1).")
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
```

---

# Explanation
- The module is completely self-contained in one Python file.
- The main class `TicTacToeGame` encapsulates the entire game logic including move validation, win/draw checks, and switching players.
- The `machine_move` method currently uses a random selection approach to choose a move; this can be extended with more advanced AI if required.
- The `run_game` function is provided for quick testing and can be connected to a UI as needed.
- The module follows a clear design suitable for backend development, and includes detailed function and method signatures with explanations.
```