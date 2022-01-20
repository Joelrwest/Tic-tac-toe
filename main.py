import random
import math

def has_won(board, player):
    return won_hor(board, player) or won_ver(board, player) or won_diag1(board, player) or won_diag2(board, player)

def won_hor(board, player):
    for row in board:
        if all(player == square for square in row):
            return True
    return False

def won_ver(board, player):
    for i in range(0, 3):
        if all(player == board[j][i] for j in range(0, 3)):
            return True
    return False

def won_diag1(board, player):
    if all(player == board[i][i] for i in range(0, 3)):
        return True
    return False

def won_diag2(board, player):
    if all(player == board[i][2 - i] for i in range(0, 3)):
        return True
    return False

# Returns True if the game is over, False otherwise
def game_is_over(X_won, O_won, board):
    return X_won or O_won or board_full(board)

# Takes in a tuple of coordinates.
# Returns True if the given coordinates are on diagonal 1.
# Returns False otherwise.
def is_on_diag1(square):
    (row, col) = square
    if row == col:
        return True
    else:
        return False

# Takes in a tuple of coordinates.
# Returns True if the given coordinates are on diagonal 2.
# Returns False otherwise.
def is_on_diag2(square):
    (row, col) = square
    if row == 2 - col:
        return True
    else:
        return False

# Checks if the current board is full of X's and O's.
# Returns True if it is, returns False if it isn't
def board_full(board):
    return len(empty_squares(board)) == 0

# Prints out the given board to the console
def print_board(board):
    # Print the top seperator
    print("-------------")

    # For each row print | X | Y | Z | where X, Y, Z are whatever the square contains.
    # Then print seperator
    for row in board:
        for square in row:
            print(f"| {square} ", end = '')
        print("|")
        print("-------------")

# Gets a command from the console. Must be entered in the form
# "X Y", where X and Y are integers in the range [0, 2]
# Clean by shortening
def get_commands(board):
    # Loop forever until we get a command
    while True:
        # Take an input and separate them by spaces
        inp = input("Please enter two integers seperated by a space:\n")
        commands = inp.split(' ')

        # Get rid of empty commands
        commands = list(filter(lambda command: command != '', commands))

        # There should be exactly two commands, otherwise we have no idea what to do
        if len(commands) != 2:
            # The input is invalid. Print an explanation and go back to the start of the loop
            print(f"You have entered {len(commands)} commands. Number of commands must be exactly two. Please try again.")
            continue
        
        # Try and convert to an int, then return a list of commands if it works nicely
        row = -1
        col = -1
        try:
            # Try to make int
            row = int(commands[0])
            col = int(commands[1])
        except:
            # Couldn't turn commands into ints, print explanation and take input again
            print("Please enter commands as integers.")
            continue        
        
        # Both row and col must be either 0, 1 or 2
        if (col or row) not in range(0, 3):
            # They're not in that range. Print explanation and try again
            print("Commands must both be either 0, 1 or 2. Please enter them again.")
        
        # Check if the square is already in use
        if board[row][col] != " ":
            print(f"This square already has a {board[row][col]} on it! Try again.")
            continue
        
        # All is good :)
        return (row, col)

# Returns a list of coordinates where a given square is
# currently empty
def empty_squares(board):
    moves = []
    for i, row in enumerate(board):
        for j, square in enumerate(row):
            if square == " ":
                moves.append((i, j))
    
    return moves

# Makes and returns an entirely separate copy of the given board
def copy_board(board):
    # Copy is initially empty
    copy = []

    # For each row, append a copy of that row to the list copy
    for row in board:
        copy.append(row.copy())
    
    # Copy == board, but has it's own memory associated
    return copy

# Returns -1 if the possition is lost at best for player,
# 0 if the position is tied, and 1 if the position is
# guaranteed won
def minimax(board, player):
    # First do the base cases

    # If player has won, return 1
    # If the other player has won, return -1 since player lost
    # If neither of those were true, and the board is full, it's a draw so return 0
    if has_won(board, player):
        return 1
    elif has_won(board, other_player(player)):
        return -1
    elif board_full(board):
        return 0

    # Initially, assume that the game is worse than lost
    eval = -math.inf

    # Find possible moves
    moves = empty_squares(board)
    
    # For each move, go deeper
    for (row, col) in moves:
        # Make the move
        board[row][col] = player

        # Find the evaluation from the other players perspective
        this_eval = -minimax(board, other_player(player))

        # Unmake the move
        board[row][col] = " "

        # If this is better than the previous best,
        # then this is the new best
        eval = max(eval, this_eval)
    
    return eval

# Return the moves with the highest eval
def best_computer_moves(board):
    # Set up the variables    
    moves = empty_squares(board)
    eval = -math.inf

    best_moves = []

    for (row, col) in moves:
        # Make this move
        board[row][col] = "O"

        # Now that computer has gone, person is the next to go.
        # Get the eval for this position.
        this_eval = -minimax(board, "X")

        # Unmake this move
        board[row][col] = " "

        # Check if this move is better than the previous best
        if this_eval > eval:
            best_moves = [(row, col)]
            eval = this_eval
        elif this_eval == eval:
            best_moves.append((row, col))
    
    # Return the best that was found
    return best_moves

# Returns the opposite player to the one given
# If the given player is invalid, raises an exception
def other_player(player):
    if player == "X":
        return "O"
    elif player == "O":
        return "X"
    else:
        raise ValueError("Given player must be either X or O")

# Returns a new, empty board
def new_board():
    board = []
    for i in range(0, 3):
        row = [" ", " ", " "]
        board.append(row)
    return board

# -----------------------------------------------------------------------------------------------------------

# Set up the board. Board is just a list of size 3. This board list in turn has 
# 3 rows each also of size 3. The elements in each row will either be "X", "O" or " ".
# The coordinates of each square are as below:

# ----------------------------
# | (0, 0) | (0, 1) | (0, 2) |
# ----------------------------
# | (1, 0) | (1, 1) | (1, 2) |
# ----------------------------
# | (2, 0) | (2, 1) | (2, 2) |
# ----------------------------

# Note that the coordinate (a, b) would correspond to board[a][b].
# Player is "X" and computer is "O".

def main():
    # Board is an intially empty list
    board = new_board()

    X_won = False
    O_won = False
    # Now is a 3x3 list with " " in each index.
    while not game_is_over(X_won, O_won, board):
        # Print the board so the player can see what's happening
        print_board(board)

        if not game_is_over(X_won, O_won, board):
            # Get the inputs from the player.
            # Note that get_commands() doesn't return
            # until a valid input is received, so theoretically
            # this could go forever.
            (row, col) = get_commands(board)
            board[row][col] = "X"
            if has_won(board, "X"):
                X_won = True
        if not game_is_over(X_won, O_won, board):
            # Get the move from the computer
            best_moves = best_computer_moves(board)
            (comp_row, comp_col) = random.choice(best_moves)
            board[comp_row][comp_col] = "O"
            if has_won(board, "O"):
                O_won = True

    print_board(board)
    print("Game is over!")

    if X_won:
        print("Player has won")
    elif O_won:
        print("Computer has won!")
    else:
        print("It's a draw")

if __name__ == "__main__":
    main()
