# Connect 4 game
<img src="https://github.com/ikteng/connect-4-game/blob/main/connect_game_image.webp" alt="Connect 4 game image" style="width:100px;height:200px;">

### Description
Connect 4 is a classic two-player connection game played on a 6x7 grid, where players take turns dropping discs of their chosen color into columns. 

### Objective
The objective is to connect four of one's own discs vertically, horizontally, or diagonally before the opponent does.

# Connect4Player Class
This class represents an AI Connect 4 player. Here's a summary of its key attributes and methods:
- board: a 6x7 grid representing the Connect 4 game board.
- pieces: a list containing the player's and AI's pieces, where 'Y' stands for yellow and 'R' for red.
- __init__(self): initializes a player object by randomly choosing a color for the player and setting up the opponent's color and depth limit for the minimax search.
- print_board(self): prints the current state of the Connect 4 board.
- place_piece(self, move, piece): places the player's or AI's piece on the board.
- make_move(self, state): selects a column for the next move using the minimax algorithm.
- succ(self, state, piece): returns a list of all possible successor states from the current board state.

# Minimax Algorithm
The minimax algorithm is implemented with alpha-beta pruning to efficiently search for the best move in the game tree.
- max_value(self, a, b, state, depth): returns the maximum value of the state.
- min_value(self, a, b, state, depth): returns the minimum value of the state.

# Heuristic Evaluation Function
The heuristic function evaluates non-terminal states and assigns scores based on potential wins.
- heuristic_game_value(self, state, piece): evaluates non-terminal states and assigns scores based on potential wins in rows, columns, and diagonals.

# Other Methods
- opponent_move(self, move): validates the opponent's next move against the internal board representation.
- game_value(self, state): checks the current board status for a win condition.
- main(): initiates the Connect 4 game, alternating between player and AI moves until a winner is determined.

# Sample Gameplay
The main() function initializes the game, prints the board, and alternates between player and AI moves. The game loop continues until there's a winner or the board is full, and the winner is announced at the end.

# Summary
This Connect 4 implementation features an AI opponent using the minimax algorithm with alpha-beta pruning. 
The heuristic evaluation function enhances the AI's decision-making in non-terminal states. The game is played through the console, and the player is prompted to choose a column for their move. 
The AI and player take turns until a winner is determined or the game ends in a draw.
