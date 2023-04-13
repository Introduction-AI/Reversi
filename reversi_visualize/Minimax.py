import random as rd
import numpy as np
import sys
import copy
import enum

WHITE = 1
NOBODY = 0
BLACK = -1

NUM_COLUMNS = 8

SEARCH_DEPTH = 3

class GamePhase(enum.Enum):
    EARLY_GAME = 1
    MID_GAME = 2
    LATE_GAME = 3

board = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1,-1, 0, 0, 0],
         [0, 0, 0,-1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],])

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1)]

class minimax():
    nodesExplored = 0

    def __init__(self, board, player = 1, remain_time = 50):
        self.board = board
        self.player = player
        self.remain_time = remain_time

    def getPlayerStoneCount(self, board, player):
        score = 0
        for i in range(8):
            for j in range(8):
                if(board[i][j] == player): score+=1
        return score

    def getGamePhase(self, board):
        chessCnt = np.count_nonzero(board)
        if chessCnt<20: 
            return GamePhase.EARLY_GAME
        elif chessCnt<=58: 
            return GamePhase.MID_GAME
        else: 
            return GamePhase.LATE_GAME
        
    def evalCorner(self, board , player):
        opponent = -1 if player == 1 else 1

        myCorners = 0
        opCorners = 0

        if(board[0][0]==player): myCorners+=1
        if(board[7][0]==player): myCorners+=1
        if(board[0][7]==player): myCorners+=1
        if(board[7][7]==player): myCorners+=1

        if(board[0][0]==opponent): opCorners+=1
        if(board[7][0]==opponent): opCorners+=1
        if(board[0][7]==opponent): opCorners+=1
        if(board[7][7]==opponent): opCorners+=1

        return 100 * (myCorners - opCorners) / (myCorners + opCorners + 1)
    
    def evalDiscDiff(self, board , player):
        opponent = -1 if player == 1 else 1

        myDiskCnt = self.getPlayerStoneCount(board, player)
        opDiskCnt = self.getPlayerStoneCount(board, opponent)

        return 100 * (myDiskCnt - opDiskCnt) / (myDiskCnt + opDiskCnt)
    
    def evalParity(self, board):
        remDisks = 64 - np.count_nonzero(board)
        return -1 if remDisks % 2 == 0 else 1
    
    def evalMobility(self, board , player):
        opponent = -1 if player == 1 else 1

        myMoveCount = len(self.get_valid_moves(board,player))
        opMoveCount = len(self.get_valid_moves(board,opponent))

        return 100 * (myMoveCount - opMoveCount) / (myMoveCount + opMoveCount + 1)
    
    def heuristic(self, board, player):

        if(self.Win(board, player) or self.Lose(board, player) or self.Tie(board, player)):
            return 1000*self.evalDiscDiff(board, player)

        if self.getGamePhase(board) == GamePhase.EARLY_GAME:
            return 1000*self.evalCorner(board,player) + 50*self.evalMobility(board,player)
        elif self.getGamePhase(board) == GamePhase.MID_GAME:
            return 1000*self.evalCorner(board,player) + 20*self.evalMobility(board,player) + 10*self.evalDiscDiff(board, player) + 100*self.evalParity(board)
        elif self.getGamePhase(board) == GamePhase.LATE_GAME:
            pass
        else:
            return 1000*self.evalCorner(board,player) + 100*self.evalMobility(board,player) + 500*self.evalDiscDiff(board, player) + 500*self.evalParity(board)
    
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

    def get_valid_moves(self,board, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(board, row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def Win(self, board, player):
        opponent = -1 if player == 1 else 1
        if ((self.getPlayerStoneCount(board, 0) == 0 and self.getPlayerStoneCount(board, player) > self.getPlayerStoneCount(board, opponent)) or self.getPlayerStoneCount(board, opponent) == 0): 
            return True
        else: return False

    def Lose(self, board, player):
        opponent = -1 if player == 1 else 1
        return True if ((self.getPlayerStoneCount(board, 0) == 0 and self.getPlayerStoneCount(board, player) < self.getPlayerStoneCount(board, opponent)) or self.getPlayerStoneCount(board, player) == 0) else False
    
    def Tie(self, board, player):
        opponent = -1 if player == 1 else 1
        return True if (self.getPlayerStoneCount(board, 0) == 0 and self.getPlayerStoneCount(board, player) == self.getPlayerStoneCount(board, opponent)) else False
    
    def countDics(self, board, player):
        num = 0
        for row in board:
            num += row.count(player)
        return num
    # def make_move(self, board, row, col, player):
    #         new_board = [row[:] for row in board]
    #         new_board[row][col] = player
            
    #         for i in range(-1, 2):
    #             for j in range(-1, 2):
    #                 if i == 0 and j == 0:
    #                     continue
                    
    #                 r = row + i
    #                 c = col + j
    #                 flipped = False
    #                 to_flip = []
                    
    #                 while r >= 0 and r < 8 and c >= 0 and c < 8:
    #                     if new_board[r][c] == 0:
    #                         break
    #                     if new_board[r][c] == player:
    #                         flipped = True
    #                         break
    #                     to_flip.append((r, c))
    #                     r += i
    #                     c += j
                    
    #                 if flipped:
    #                     for (r, c) in to_flip:
    #                         new_board[r][c] = player
            
    #         return new_board
    def make_move(self, board, move ,player):
        newboard = [row[:] for row in board]

        newboard[move[0]][move[1]] = player
        flip = self.getReversePoints(newboard,player,move[0],move[1])
        for point in flip:
            newboard[point[0]][point[1]] = player

        return newboard
    def getReversePoints(self, board, player, row, col):
        allReversePoints = []

        mrow = 0 ; mcol = 0
        opponent = -1 if player == 1 else 1
        #move up
        flip_list = []
        mrow = row - 1
        mcol = col
        while (mrow>0 and board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mrow-=1

        if (mrow>=0 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list
        #move down
        flip_list = []
        mrow = row + 1
        mcol = col
        
        while (mrow<7 and  board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mrow+=1

        if(mrow<=7 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list
        #move left
        flip_list = []
        mrow = row
        mcol = col - 1
        while (mcol>0 and board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mcol-=1

        if(mcol>=0 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list
        

        #move right
        flip_list = []
        mrow = row
        mcol = col + 1
        while(mcol<7 and board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mcol+=1
        
        if(mcol<=7 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list
        

        #move up left
        flip_list = []
        mrow = row - 1
        mcol = col - 1
        while(mrow>0 and mcol>0 and board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mrow-=1
            mcol-=1
        
        if(mrow>=0 and mcol>=0 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list
        

        #move up right
        flip_list = []
        mrow = row - 1
        mcol = col + 1
        while(mrow>0 and mcol<7 and board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mrow-=1
            mcol+=1
        
        if(mrow>=0 and mcol<=7 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list
        

        #move down left
        flip_list = []
        mrow = row + 1
        mcol = col - 1
        while(mrow<7 and mcol>0 and board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mrow+=1
            mcol-=1
        
        if(mrow<=7 and mcol>=0 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list

        #move down right
        flip_list = []
        mrow = row + 1
        mcol = col + 1
        while(mrow<7 and mcol<7 and board[mrow][mcol] == opponent):
            flip_list.append((mrow,mcol))
            mrow+=1
            mcol+=1
        
        if(mrow<=7 and mcol<=7 and board[mrow][mcol] == player and len(flip_list)>0):
            allReversePoints += flip_list

        return allReversePoints;
    
    # def heuristic(self, board, player):
    #     h = [
    #         [20, -3, 11, 8, 8, 11, -3, 20],
    #         [-3, -7, -4, 1, 1, -4, -7, -3],
    #         [11, -4, 2, 2, 2, 2, -4, 11],
    #         [8, 1, 2, -3, -3, 2, 1, 8],
    #         [8, 1, 2, -3, -3, 2, 1, 8],
    #         [11, -4, 2, 2, 2, 2, -4, 11],
    #         [-3, -7, -4, 1, 1, -4, -7, -3],
    #         [20, -3, 11, 8, 8, 11, -3, 20]
    #     ]
    #     X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
    #     Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
    #     myself, opp = 0, 0
    #     myself_front, opp_front = 0, 0
    #     f = 0
    #     p, c, l, m, f, d = 0, 0, 0, 0, 0, 0

    #     #  Piece difference, frontier disks and disk squares
    #     for y in range(8):
    #         for x in range(8):
    #             if board[y][x] == player:
    #                 d += h[y][x]*player
    #                 if player > 0: myself +=1 
    #                 else: opp +=1

    #             if board[y][x] == '0':
    #                 for i in range(8):
    #                     x = x + X1[i]
    #                     y = y + Y1[i]

    #                     if ((x >= 0) and (x < 8) and (y >=0) and (y < 8) and board[y][x] == '0'):
    #                         if player > 0: myself_front +=1 
    #                         else: opp_front +=1
    #                         break

    #     if (myself > opp): p += (100 * myself)/(myself + opp)
    #     elif (myself < opp): p += -(100 * opp)/(myself + opp)

    #     if(myself > opp):
    #         f += -(100.0 * myself)/(myself + opp)
    #     elif(myself < opp):
    #         f += (100.0 * opp)/(myself + opp)

    #     # Corner occupancy
    #     myself, opp = 0, 0
    #     if (board[0][0] == player) or \
    #     (board[7][0] == player) or \
    #     (board[0][7] == player) or \
    #     (board[7][7] == player):
    #         if player > 0: myself +=1 
    #         else: opp +=1
    #     c = 25*(myself - opp)

    #     # Corner closeness
    #     myself, opp = 0, 0
    #     if(board[0][0] == '0'):
    #         if (board[1][0] == player) or \
    #         (board[1][1] == player) or \
    #         (board[0][1] == player):
    #             if player > 0: myself +=1 
    #             else: opp +=1
        
    #     if(board[7][0] == '0'):
    #         if (board[6][0] == player) or \
    #         (board[6][1] == player) or \
    #         (board[7][1] == player):
    #             if player > 0: myself +=1 
    #             else: opp +=1
        
    #     if(board[0][7] == '0'):
    #         if (board[1][7] == player) or \
    #         (board[1][6] == player) or \
    #         (board[0][6] == player):
    #             if player > 0: myself +=1 
    #             else: opp +=1
            
    #     if(board[7][7] == '0'):
    #         if (board[7][6] == player) or \
    #         (board[6][6] == player) or \
    #         (board[6][7] == player):
    #             if player > 0: myself +=1 
    #             else: opp +=1
        
    #     l  += -12.5*(myself - opp)

    #     # Mobility
    #     myself, opp = 0, 0
    #     myself = len(self.get_valid_moves(board, player))
    #     opp = len(self.get_valid_moves(board, player*-1))
    #     if (myself > opp):
    #         m += (100 * myself)/(myself + opp)
    #     else:
    #         m += -(100 * opp)/(myself + opp)

    #     score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)

    #     return score
    
    # def minimax_value(self, board, white_turn, search_depth, alpha, beta):
    #     if search_depth == 0:
    #         return self.heuristic(board, 1)
    #     if self.Tie(board, 1):
    #         return 0
    #     elif self.Win(board, 1):
    #         return 100000
    #     elif self.Lose(board, 1):
    #         return -100000
    #     else:
    #             pass # No game condition met, continue searching down the decision tree.
        
    #     if white_turn:
    #         maxScore = -sys.maxsize
    #         legal_moves = self.get_valid_moves(board, 1)

    #         if len(legal_moves) == 0:
    #             maxScore = self.minimax_value(board, False, search_depth, alpha, beta)

    #         else:
    #             for move in legal_moves:
    #                 new_board = self.make_move(board, move[0], move[1], 1) # Get the new board state
    #                 score = self.minimax_value(new_board, False, search_depth - 1, alpha, beta)
    #                 maxScore = max(maxScore, score)
    #                 alpha = max(alpha, score)
    #                 if beta <= alpha:
    #                     break
    #         return maxScore

    #     else:
    #         minScore = sys.maxsize
    #         legal_moves = self.get_valid_moves(board, -1)
    #         if len(legal_moves) == 0:
    #             minScore = self.minimax_value(board, True, search_depth, alpha, beta)
            
    #         else:
    #             for move in legal_moves:
    #                 new_board = self.make_move(board, move[0], move[1], -1) # Get the new board state
    #                 score = self.minimax_value(new_board, True, search_depth - 1, alpha, beta)
    #                 minScore = min(minScore, score)
    #                 beta = min(beta, score)
    #                 if beta <= alpha:
    #                     break
    #         return minScore
    def minimax_value(self, node, player, player_turn, search_depth, alpha, beta):
        global nodesExplored
        nodesExplored+=1
        if (search_depth == 0 or self.Win(node, player) or self.Lose(node, player) or self.Tie(node, player)):
            return self.heuristic(node, player)
        opponent = -1 if player == 1 else 1
        
        if((player_turn == True and len(self.get_valid_moves(node,player)) == 0) or (player_turn == False and len(self.get_valid_moves(node,opponent)) == 0)):
            return self.minimax_value(node, player, not player_turn, search_depth-1 ,alpha,beta)
        score = 0
        if(player_turn == True):
            score = -100000
            for move in self.get_valid_moves(node,player):
                newNode = self.make_move(node, move, player)
                childScore = self.minimax_value(newNode, player, not player_turn, search_depth-1, alpha,beta)
                if (childScore == None): childScore = 0
                if(childScore > score): score = childScore
                if(score > alpha): alpha = score
                if(beta <= alpha): break
        else:
            score = 100000
            for move in self.get_valid_moves(node,opponent):
                newNode = self.make_move(node, move, opponent)
                childScore = self.minimax_value(newNode, player, player_turn, search_depth-1, alpha,beta)
                if (childScore == None): childScore = 0
                if(childScore < score): score = childScore
                if(score < beta): beta = score
                if(beta <= alpha): break
        return score
    def select_moves(self, board, player, remain_time):

        global nodesExplored
        nodesExplored = 0
        bestScore = -100000
        bestMove = None
        for move in self.get_valid_moves(board,player):
            newNode = self.make_move(board, move, player)
            childScore = self.minimax_value(newNode,player, True, SEARCH_DEPTH, -100000, 100000)
            if (childScore == None): break
            if(childScore > bestScore):
                bestScore = childScore
                bestMove = move
        return bestMove
# a = minimax(board, 1, 50)
# b = a.select_moves(board, 1, 50)
# print(b)
#minimax(board, 1, 50)

def select_move(cur_state, player_to_move, remain_time):
    a = minimax(cur_state, player_to_move, remain_time)
    b = a.select_moves(cur_state, player_to_move, remain_time)
    return b