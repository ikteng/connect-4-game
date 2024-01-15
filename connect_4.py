import random
import copy

class Connect4Player:
    """ An object representation for an AI Connect 4 player"""
    board = [[' ' for _ in range(7)] for _ in range(6)]
    pieces = ['Y', 'R'] # Y: yellow, R: red

    def __init__(self):
        """ Initializes an AI Connect 4 player object by randomly choosing whether they are using red or yellow colored pieces"""
        # randomly choose a color for player
        self.my_piece = random.choice(self.pieces)
        # set opponent (AI) color
        self.ai_piece = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        # set depth limit for minimax search
        self.depth = 3

    def print_board(self):
        """ Prints the current state of the Connect 4 board"""
        for row in range(len(self.board)):
            line=""
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("1 2 3 4 5 6 7\n")

    def place_piece(self, move, piece):
        """ Places the player's or AI's piece on the board"""
        col = move[0][1]  # Accessing the second element of the tuple for column index
        for row in range(5, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = piece
                break


    def make_move(self, state):
        """ Selects a column for the next move"""
        best_value = float("-inf")
        best_state = None
        for successor in self.succ(state, self.my_piece):
            current_value = self.min_value(float("-inf"), float("inf"), successor, 1)
            if current_value > best_value:
                best_value = current_value
                best_state = successor

        move = []
        for i in range(6):  # Adjust loop range to match the board dimensions
            for j in range(7):
                if state[i][j] == ' ' and state[i][j] != best_state[i][j]:
                    (row, col) = (i, j)
                    # ensure the destination (row, col) tuple is at the beginning of the move list
                    move.insert(0, (row, col))

        return move

    def succ(self, state, piece):
        """ Returns a list of all possible successor states from board state"""
        successors = []
        
        for row in range(6):
            for col in range(7):
                state_copy = copy.deepcopy(state)  # Create a copy of the state
                if state_copy[row][col] == ' ':
                    # add a new piece of the current player's type to the board
                    state_copy[row][col] = piece
                    successors.append(state_copy)

        return successors

    # minimax algorithm
    #####################################################################################
    def max_value(self, a, b, state, depth):
        """ Returns the maximum value of the state"""
        if self.game_value(state) != 0:
            return self.game_value(state)

        if depth >= self.depth:
            return self.heuristic_game_value(state, self.my_piece)

        successors = self.succ(state, self.my_piece)
        for successor in successors:
            a = max(a, self.min_value(a, b, successor, depth + 1))
            # alpha pruning
            if a >= b:
                return b
        return a

    def min_value(self, a, b, state, depth):
        """ Returns the minimum value of the state"""
        if self.game_value(state) != 0:
            return self.game_value(state)

        if depth >= self.depth:
            return self.heuristic_game_value(state, self.ai_piece)

        successors = self.succ(state, self.ai_piece)
        for successor in successors:
            b = min(b, self.max_value(a, b, successor, depth + 1))
            # beta pruning
            if a >= b:
                return a
        return b
    
    #####################################################################################
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation"""
        col = move[0]
        if col < 0 or col >= 7 or self.board[0][col] != ' ':
            raise Exception("Illegal move: Column is full or out of bounds")
        # find the lowest empty row in the selected column
        for row in range(5, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = self.ai_piece
                break

    def game_value(self, state):
        """ Checks the current board status for a win condition"""
        for row in range(6):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col + 1] == state[row][col + 2] == state[row][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        for col in range(7):
            for row in range(3):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col] == state[row + 2][col] == state[row + 3][col]:
                    return 1 if state[row][col] == self.my_piece else -1

        for row in range(3):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col + 1] == state[row + 2][col + 2] == state[row + 3][col + 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        for row in range(3):
            for col in range(3, 7):
                if state[row][col] != ' ' and state[row][col] == state[row + 1][col - 1] == state[row + 2][col - 2] == state[row + 3][col - 3]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0  # no winner yet

    # Evaluate all non-terminal states
    def heuristic_game_value(self, state, piece):
        # Maximal positive score (1) -> terminal state for AI player
        # Minimal negative score (-1) -> terminal state for opponent
        factor = 1 if piece == self.my_piece else -1

        # Check whether the state is a terminal state
        if self.game_value(state) != 0:
            return self.game_value(state)

        # Check for horizontal wins
        max_row_score = 0
        for row in state:
            for col in range(4):
                row_score = 0
                for k in range(4):
                    if row[col + k] == piece:
                        row_score += 0.25
                    elif row[col + k] != ' ':
                        row_score -= 0.05

                if row_score > max_row_score:
                    max_row_score = row_score

        # Check for vertical wins
        max_col_score = 0
        for col in range(7):
            for row in range(3):
                col_score = 0
                for k in range(4):
                    if state[row + k][col] == piece:
                        col_score += 0.25
                    elif state[row + k][col] != ' ':
                        col_score -= 0.05

                if col_score > max_col_score:
                    max_col_score = col_score

        # Check for diagonal wins (\)
        max_diag1_score = 0
        for row in range(3):
            for col in range(4):
                diag1_score = 0
                for k in range(4):
                    if state[row + k][col + k] == piece:
                        diag1_score += 0.25
                    elif state[row + k][col + k] != ' ':
                        diag1_score -= 0.05

                if diag1_score > max_diag1_score:
                    max_diag1_score = diag1_score

        # Check for diagonal wins (/)
        max_diag2_score = 0
        for row in range(3):
            for col in range(3, 7):
                diag2_score = 0
                for k in range(4):
                    if state[row + k][col - k] == piece:
                        diag2_score += 0.25
                    elif state[row + k][col - k] != ' ':
                        diag2_score -= 0.05

                if diag2_score > max_diag2_score:
                    max_diag2_score = diag2_score

        # Potential variations/errors for AI
        max_row_score += random.uniform(-0.02, 0.02)
        max_col_score += random.uniform(-0.02, 0.02)
        max_diag1_score += random.uniform(-0.02, 0.02)
        max_diag2_score += random.uniform(-0.02, 0.02)

        # Weighted sum of features
        heuristic = max(max_row_score, max_col_score, max_diag1_score, max_diag2_score)
        return factor * heuristic

# sample gameplay
###############################################################################################################
def main():
    print('Welcome to Connect 4 Game!')
    ai = Connect4Player()
    turn = 0

    # game loop
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at column " + str(move))
        else:
            move_made = False
            ai.print_board()
            print(ai.ai_piece + "'s turn")
            while not move_made:
                player_move = int(input("Choose a column (1-7): "))-1
                while str(player_move) not in "0123456":
                    player_move = int(input("Choose a column (1-7): ")) - 1
                try:
                    ai.opponent_move([player_move])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
