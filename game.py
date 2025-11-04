import numpy as np

rows = 6
columns = 7
empty_cell = 0
players_piece = 1
ai_piece = 2

def create_board():
  return np.zeros((rows,columns), dtype=int)

def drop_piece(board, row, col, piece):
  board[row][col] = piece

def valid_loc(board, col):
  valid = 0 <= col < columns and board[0][col] == empty_cell
  return valid

def next_available_row(board, col):
  for row in range(rows - 1, -1, -1):
    if board[row][col] == empty_cell:
      return row
  return None

def is_valid(board):
  valid_locations = []
  for col in range(columns):
    if valid_loc(board, col):
      valid_locations.append(col)
  return valid_locations


def win_move(board, piece):
  #yatay
  for row in range(rows):
    for col in range(columns - 3):
      if (board[row][col] == piece and board[row][col + 1] == piece and board[row][col + 2] == piece and board[row][col + 3] == piece):
        return True
      
  #dikey   
  for col in range(columns):
    for row in range(rows - 3):
      if (board[row][col] == piece and board[row + 1][col] == piece and board[row + 2][col] == piece and board[row + 3][col] == piece):
        return True
      
  #diagonal
  for row in range(rows - 3):
    for col in range(columns - 3):
      if board[row][col] == piece and board[row + 1][col + 1] == piece and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece:
        return True

  for row in range(3, rows):
    for col in range(columns - 3):
      if board[row][col] == piece and board[row - 1][col + 1] == piece and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece:
        return True
      
  return False

def terminal_node(board):
  return win_move(board, players_piece) or win_move(board, ai_piece) or len(is_valid(board)) == 0
