
import random as rd
import numpy as np
import sys
import copy
import pygame as pg

WHITE = 1
NOBODY = 0
BLACK = -1

NUM_COLUMNS = 8

CELL_SIZE = 60

board = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1,-1, 0, 0, 0],
         [0, 0, 0,-1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],]

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)]

class Agents:
    def __init__(self):
        pass
    def is_valid_move(self, board, row, col, player):
        if board[row][col] != 0:
            return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                r = row + i
                c = col + j
                found_opponent = False
                while r >= 0 and r < 8 and c >= 0 and c < 8:
                    if board[r][c] == 0:
                        break
                    if board[r][c] == player:
                        if found_opponent:
                            return True
                        break
                    found_opponent = True
                    r += i
                    c += j
        return False
    def get_valid_moves(self, board, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(board, row, col, player):
                    valid_moves.append((row, col))
        return valid_moves
    
    def random_agent(self, cur_state, player_to_move, remain_time):
        
        valid_moves = self.get_valid_moves(cur_state,player_to_move)
        if valid_moves == []: return None
        else: return rd.choice(valid_moves)


    def manual_agent(self, cur_state, player_to_move, remain_time):
        valid_moves = self.get_valid_moves(cur_state,player_to_move)
        while True:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    print("row, col: ", row, col)
                    if (row, col) in valid_moves:
                        return row, col                    
        