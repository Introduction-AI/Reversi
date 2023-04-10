
import random as rd

board = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1,-1, 0, 0, 0],
         [0, 0, 0,-1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],]

def minimax(board, player, remain_time):
    def is_valid_move(board, row, col, player):
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

    def get_valid_moves(board, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if is_valid_move(board, row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def Win(board, player):
        return True if (sum(map(sum, board))*player > 0) else False

    def countDics(board, player):
        num = 0
        for row in board:
            num += row.count(player)
        return num

    def heuristic(board, player):
        h = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]
        X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y1 = [0, 1, 1, 1, 0, -1, -1, -1]
        self, opp = 0, 0
        self_front, opp_front = 0, 0
        f = 0
        p, c, l, m, f, d = 0, 0, 0, 0, 0, 0

        #  Piece difference, frontier disks and disk squares
        for y in range(8):
            for x in range(8):
                if board[y][x] == player:
                    d += h[y][x]*player
                    if player > 0: self +=1 
                    else: opp +=1

                if board[y][x] == '0':
                    for i in range(8):
                        x = x + X1[i]
                        y = y + Y1[i]

                        if ((x >= 0) and (x < 8) and (y >=0) and (y < 8) and board[y][x] == '0'):
                            if player > 0: self_front +=1 
                            else: opp_front +=1
                            break

        if (self > opp): p += (100 * self)/(self + opp)
        elif (self < opp): p += -(100 * opp)/(self + opp)

        if(self > opp):
            f += -(100.0 * self)/(self + opp)
        elif(self < opp):
            f += (100.0 * opp)/(self + opp)

        # Corner occupancy
        self, opp = 0, 0
        if (board[0][0] == player) or \
        (board[7][0] == player) or \
        (board[0][7] == player) or \
        (board[7][7] == player):
            if player > 0: self +=1 
            else: opp +=1
        c = 25*(self - opp)

        # Corner closeness
        self, opp = 0, 0
        if(board[0][0] == '0'):
            if (board[1][0] == player) or \
            (board[1][1] == player) or \
            (board[0][1] == player):
                if player > 0: self +=1 
                else: opp +=1
        
        if(board[7][0] == '0'):
            if (board[6][0] == player) or \
            (board[6][1] == player) or \
            (board[7][1] == player):
                if player > 0: self +=1 
                else: opp +=1
        
        if(board[0][7] == '0'):
            if (board[1][7] == player) or \
            (board[1][6] == player) or \
            (board[0][6] == player):
                if player > 0: self +=1 
                else: opp +=1
            
        if(board[7][7] == '0'):
            if (board[7][6] == player) or \
            (board[6][6] == player) or \
            (board[6][7] == player):
                if player > 0: self +=1 
                else: opp +=1
        
        l  += -12.5*(self - opp)

        # Mobility
        self, opp = 0, 0
        self = len(get_valid_moves(board, player))
        opp = len(get_valid_moves(board, player*-1))
        if (self > opp):
            m += (100 * self)/(self + opp)
        else:
            m += -(100 * opp)/(self + opp)

        score = (10 * p) + (801.724 * c) + (382.026 * l) + (78.922 * m) + (74.396 * f) + (10 * d)

        return score

    a = heuristic(board, 1)
    print(a)

minimax(board, 1, 50)

def random_agent(cur_state, player_to_move, remain_time):
    def is_valid_move(board, row, col, player):
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
    def get_valid_moves(board, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if is_valid_move(board, row, col, player):
                    valid_moves.append((row, col))
        return valid_moves
    valid_moves = get_valid_moves(cur_state,player_to_move)
    if valid_moves == []: return None
    else: return rd.choice(valid_moves)
def move_by_yourself(cur_state, player_to_move, remain_time):
    def is_valid_move(board, row, col, player):
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
    def get_valid_moves(board, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if is_valid_move(board, row, col, player):
                    valid_moves.append((row, col))
        return valid_moves
    valid_moves = get_valid_moves(cur_state,player_to_move)
    if valid_moves == []: return None
    print(valid_moves)
    a = int(input())
    return valid_moves[a]