class Connect4:
    def __init__(self):
        self.board = [[" " for _ in range(7)] for _ in range(6)]  # 6 rows and 7 columns
        self.current_player = "X"  # Player X always starts
        self.game_over = False

    def display_board(self):
        for row in self.board:
            print("|" + "|".join(row) + "|")
        print(" " + "-" * 15)
        print(" 0  1  2  3  4  5  6")

    def make_move(self, column):
        if self.game_over:
            return False

        if column < 0 or column > 6:
            return False

        # Place the token in the lowest available row in the chosen column
        for row in range(5, -1, -1):
            if self.board[row][column] == " ":
                self.board[row][column] = self.current_player
                if self.check_winner():
                    self.game_over = True
                    return self.current_player
                self.current_player = "O" if self.current_player == "X" else "X"
                return True

        return False

    def check_winner(self):
        # Check all rows
        for row in range(6):
            for col in range(4):  # Only need to check starting positions for 4 in a row
                if self.board[row][col] == self.current_player and \
                   self.board[row][col + 1] == self.current_player and \
                   self.board[row][col + 2] == self.current_player and \
                   self.board[row][col + 3] == self.current_player:
                    return True

        # Check all columns
        for col in range(7):
            for row in range(3):  # Only need to check starting positions for 4 in a column
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col] == self.current_player and \
                   self.board[row + 2][col] == self.current_player and \
                   self.board[row + 3][col] == self.current_player:
                    return True

        # Check diagonals (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col + 1] == self.current_player and \
                   self.board[row + 2][col + 2] == self.current_player and \
                   self.board[row + 3][col + 3] == self.current_player:
                    return True

        # Check diagonals (top-right to bottom-left)
        for row in range(3):
            for col in range(3, 7):
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col - 1] == self.current_player and \
                   self.board[row + 2][col - 2] == self.current_player and \
                   self.board[row + 3][col - 3] == self.current_player:
                    return True

        return False

# Initialize the game
connect4 = Connect4()

# Display the initial board
connect4.display_board()

moves = []
for move in moves:
    print(f"Player {connect4.current_player} plays column {move}")
    x = connect4.make_move(move)
    if x == True:
        connect4.display_board()
    elif x in {"X", "O"}:
        break
    else:
        print("Move failed.")
        
import copy
import random
def immediate_win_or_block():
    global connect4
    # Check for immediate winning move for the current player
    for column in range(7):
        temp_game = copy.deepcopy(connect4)
        if temp_game.make_move(column):  # Simulate move
            if temp_game.check_winner():  # Check if it leads to a win
                return column  # Play this column to win immediately

    # Check for immediate block (prevent opponent's win)
    opponent = "O" if connect4.current_player == "X" else "X"
    for column in range(7):
        temp_game = copy.deepcopy(connect4)
        if temp_game.make_move(column):  # Simulate opponent's move
            if temp_game.check_winner():  # Check if it leads to their win
                return column  # Block this column

    # No immediate win or block required
    return None

def negamax(depth, alpha, beta, color):
    global connect4
    if depth == 0 or connect4.check_winner():
        # Score: 100 for win, -100 for loss, or 0 for neutral
        if connect4.check_winner():
            return -100
        return 0
    
    value = -1000
    r = range(7)
    attack = immediate_win_or_block()
    if attack is not None:
      r = [attack]
    for move in r:  # Ensure all 7 columns are considered
        
        old = copy.deepcopy(connect4)  # Save the current state
        if connect4.make_move(move):  # Validate move
            value = max(value, -negamax(depth - 1, -beta, -alpha, -color))  # Recursive call
            alpha = max(alpha, value)
            if alpha >= beta:  # Prune the branch
                connect4 = old
                break
        connect4 = old  # Restore game state after exploring this move
    return value

def play(depth):
  global connect4
  best_value = -1000
  best_move = None
  r = list(range(7))
  random.shuffle(r)
  attack = immediate_win_or_block()
  if attack is not None:
    r = [attack]
  for move in r:  # Ensure all 7 columns are considered
      old = copy.deepcopy(connect4)  # Save the current state
      if connect4.make_move(move) != False:  # Validate move
          score = -negamax(depth, -1000, 1000,  1)  # Run negamax for depth 2
          if score > best_value:
              best_value = score
              best_move = move
          connect4 = old
  print(f"The best move is column {best_move} with a score of {best_value}.")
  connect4.make_move(best_move)
  connect4.display_board()

while not connect4.check_winner():
  play(5)
  if connect4.check_winner():
    break
  connect4.make_move(int(input("enter move: ")))
