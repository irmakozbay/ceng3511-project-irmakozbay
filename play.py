import math
import pygame
import sys

from game import create_board, drop_piece, valid_loc, next_available_row, is_valid, win_move, rows, columns, empty_cell, players_piece, ai_piece

from minimax_ai import minimax, pick_the_best_loc

square_size = 140
radius = int(square_size/2 - 5)
width = columns * square_size
height = (rows + 1) * square_size
pink = (255, 192, 203)
cream = (255, 253, 208)
baby_blue = (137, 207, 240)
yellow = (255, 232, 102)  

pygame.init()
screen = pygame.display.set_mode((width,height))
font = pygame.font.SysFont("monospace", 40)

def draw_board(board):
  for col in range(columns):
    for row in range(rows):
      pygame.draw.rect(screen, pink, (col*square_size, row*square_size + square_size, square_size, square_size))
      pygame.draw.circle(screen, cream, (int(col*square_size + square_size/2), int(row*square_size + square_size + square_size/2)), radius)

  for col in range(columns):
    for row in range(rows):
      if board[row][col] == players_piece:
        pygame.draw.circle(screen, baby_blue, (int(col*square_size + square_size/2), height - int((row + 1)*square_size - square_size/2)), radius)
      
      elif board[row][col] == ai_piece:
        pygame.draw.circle(screen, yellow,(int(col*square_size + square_size/2),height - int((row+1)*square_size - square_size/2)),radius)

  pygame.display.update()

def main():
  board = create_board()
  game_ended = False
  turn = 0

  draw_board(board)
  pygame.display.update()

  while not game_ended:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.MOUSEMOTION:
        pygame.draw.rect(screen, cream, (0, 0, width, square_size))
        position_x = event.pos[0]
        if turn == 0:
          pygame.draw.circle(screen, baby_blue, (position_x, int(square_size/2)), radius)
      pygame.display.update()

      if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen, cream, (0, 0, width, square_size))
        if turn == 0:
          position_x = event.pos[0]
          col = int(math.floor(position_x/square_size))
          if valid_loc(board, col):
            row = next_available_row(board, col)
            drop_piece(board, row, col, players_piece)
            if win_move(board, players_piece):
              label = font.render("You Win!", 1, pink)
              screen.blit(label, (40, 10))
              game_ended = True
            turn = 1
            draw_board(board)

    if turn == 1 and not game_ended:
      pygame.time.wait(500)
      col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)
      if col == None:
        col = pick_the_best_loc(board, ai_piece)
      if valid_loc(board, col):
        row = next_available_row(board, col)
        drop_piece(board, row, col, ai_piece)
        if win_move(board, ai_piece):
          label = font.render("AI Wins!", 1, yellow)
          screen.blit(label, (40, 10))
          game_ended = True
        draw_board(board)
        turn = 0

    if game_ended:
      pygame.display.update()
      pygame.time.wait(3000)
      pygame.quit()
      sys.exit()

if __name__ == "__main__":
  main()
  