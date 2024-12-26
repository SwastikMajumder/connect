player = int(input("player: "))
class Connect4:
    def __init__(self):
        self.board = [[" " for _ in range(7)] for _ in range(6)]  
        self.current_player = "X"  
        self.game_over = False
    def display_board(self):
        for row in self.board:
            print("|" + "|".join(row) + "|")
        print(" " + "-" * 15)
        print(" 0 1 2 3 4 5 6")
    def make_move(self, column):
        if self.game_over:
            return False
        if column < 0 or column > 6:
            return False
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
        for row in range(6):
            for col in range(4):  
                if self.board[row][col] == self.current_player and \
                   self.board[row][col + 1] == self.current_player and \
                   self.board[row][col + 2] == self.current_player and \
                   self.board[row][col + 3] == self.current_player:
                    return True
        for col in range(7):
            for row in range(3):  
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col] == self.current_player and \
                   self.board[row + 2][col] == self.current_player and \
                   self.board[row + 3][col] == self.current_player:
                    return True
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col + 1] == self.current_player and \
                   self.board[row + 2][col + 2] == self.current_player and \
                   self.board[row + 3][col + 3] == self.current_player:
                    return True
        for row in range(3):
            for col in range(3, 7):
                if self.board[row][col] == self.current_player and \
                   self.board[row + 1][col - 1] == self.current_player and \
                   self.board[row + 2][col - 2] == self.current_player and \
                   self.board[row + 3][col - 3] == self.current_player:
                    return True
        return False
connect4 = Connect4()
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
    for column in range(7):
        temp_game = copy.deepcopy(connect4)
        if temp_game.make_move(column):  
            if temp_game.check_winner():  
                return column  
    opponent = "O" if connect4.current_player == "X" else "X"
    for column in range(7):
        temp_game = copy.deepcopy(connect4)
        if temp_game.make_move(column):  
            if temp_game.check_winner():  
                return column  
    return None
def count_adjacent_coins(board, player):
    rows = len(board)
    cols = len(board[0])
    count = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]  
    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == player:  
                for dx, dy in directions:
                    x, y = i + dx, j + dy
                    if in_bounds(x, y) and board[x][y] == player:
                        count += 1
    return count
def negamax(depth, alpha, beta, color):
    global connect4
    global player
    if depth == 0 or connect4.check_winner():
        if connect4.check_winner():
            return -500 - depth
        if player == 1:
            return -color * count_adjacent_coins(connect4.board, "X")
        else:
            return color * count_adjacent_coins(connect4.board, "O")
    value = -1000
    r = range(7)
    attack = immediate_win_or_block()
    if attack is not None:
      r = [attack]
    for move in r:  
        old = copy.deepcopy(connect4)  
        if connect4.make_move(move):  
            value = max(value, -negamax(depth - 1, -beta, -alpha, -color))  
            alpha = max(alpha, value)
            if alpha >= beta:  
                connect4 = old
                break
        connect4 = old  
    return value
import time
def play(depth):
  global connect4
  best_value = -1000
  best_move = None
  r = list(range(7))
  random.shuffle(r)
  attack = immediate_win_or_block()
  if attack is not None:
    r = [attack]
  for move in r:  
      old = copy.deepcopy(connect4)  
      if connect4.make_move(move) != False:  
          score = -negamax(depth, -1000, 1000,  player)  
          if score > best_value:
              best_value = score
              best_move = move
          connect4 = old
  print(f"The best move is column {best_move} with a score of {best_value}.")
  return best_move
def deepen(start):
  global connect4
  x = None
  for d in range(2,50):
      x = play(d)
      if time.time() - start > 3:
          connect4.make_move(x)
          connect4.display_board()
          return
  connect4.make_move(x)
  connect4.display_board()
if player == 1:
    while not connect4.check_winner():
      deepen(time.time())
      if connect4.check_winner():
        break
      connect4.make_move(int(input("enter move: ")))
else:
    while not connect4.check_winner():
      connect4.make_move(int(input("enter move: ")))
      if connect4.check_winner():
        break
      deepen(time.time())
