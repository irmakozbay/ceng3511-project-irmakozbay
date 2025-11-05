import random
import math
import numpy as np

from game import rows, columns, empty_cell, players_piece, ai_piece, drop_piece, next_available_row, is_valid, win_move, terminal_node

window_length = 4

def score(window, piece):
  score_val = 0
  if piece == ai_piece:
    opponent = players_piece
  else:
    opponent = ai_piece

  if window.count(piece) == 4:
    score_val += 100
  elif window.count(piece) == 3 and window.count(empty_cell) == 1:
    score_val += 5
  elif window.count(piece) == 2 and window.count(empty_cell) == 2:
    score_val += 2

  if window.count(opponent) == 3 and window.count(empty_cell) == 1:
    score_val -= 4

  return score_val

def score_pos(board, piece):
  score_val = 0
  center = []
  for i in list(board[:,columns//2]):
    center.append(int(i))
  center_count = center.count(piece)
  score_val += center_count * 3

  for row in range(rows):
    rows_list = list(board[row])
    for col in range(columns - 3):
      window = rows_list[col:col + window_length]
      score_val += score(window, piece)

  for col in range(columns):
    cols_list = list(board[:, col])
    for row in range(rows - 3):
      window = cols_list[row:row + window_length]
      score_val += score(window,piece)

  for row in range(rows - 3):
    for col in range(columns - 3):
      window = []
      for i in range(window_length):
        window.append(int(board[row + i][col + i]))
      score_val += score(window, piece)

  for row in range(rows - 3):
    for col in range(columns - 3):
      window = []
      for i in range(window_length):
        window.append(int(board[row + 3 - i][col + i]))
      score_val += score(window, piece)

  return score_val

def minimax(board, depth, alpha, beta, maximizing):
  valid_locs = is_valid(board)
  is_terminal = terminal_node(board)

  if depth == 0 or is_terminal:
    if is_terminal:
      if win_move(board, ai_piece):
        return (None, 10**12)
      elif win_move(board, players_piece):
        return (None, -10**12)
      else:
        return (None, 0)
    else:
      return (None, score_pos(board, ai_piece))

  if maximizing:
    value = -math.inf
    best_col = random.choice(valid_locs)
    for col in valid_locs:
      row = next_available_row(board, col)
      temp = board.copy()
      drop_piece(temp, row, col, ai_piece) 
      updated_score = minimax(temp, depth-1, alpha, beta, False)[1]
      if updated_score > value: 
        value = updated_score
        best_col = col
      alpha = max(alpha, value)
      if alpha >= beta:
        break
    return best_col, value

  else:
    value = math.inf
    best_col = random.choice(valid_locs)
    for col in valid_locs:
      row = next_available_row(board, col)
      temp = board.copy()
      drop_piece(temp, row, col, players_piece)
      updated_score = minimax(temp, depth-1, alpha, beta, True)[1]
      if updated_score < value:
        value = updated_score
        best_col = col
      beta = min(beta, value)
      if alpha >= beta:
        break
    return best_col, value


def pick_the_best_loc(board, piece):
  valid_locs = is_valid(board)
  best_score = -math.inf
  best_col = random.choice(valid_locs)
  for col in valid_locs:
    row = next_available_row(board, col)
    temp = board.copy()
    drop_piece(temp, row, col, piece)
    score_val = score_pos(temp, piece)
    if score_val > best_score:
      best_score = score
      best_col = col
  return best_col
      