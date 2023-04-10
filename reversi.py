import queue
import timeit
import copy

time = 0
board_size = 8

class Move:
    def __init__(self, position, setOfPoint):
        self.position = position

class State:
    def __init__(self, board: list):
        self.board = copy.deepcopy(board)

# Hàm gán tọa độ vào quân cờ
def setBoard(board, player):
    result = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == player:
                result.append((i, j))
    return result

# Hàm Kiểm tra người chơi chiến thắng (X)
def Win(board):
    return True if (sum(map(sum, board)) > 0) else False

# Hàm Kiểm tra đối phương chiến thắng (O)
def Lose(board):
    return True if (sum(map(sum, board)) > 0) else False

# Hàm sao chép ma trận bàn cờ
def copyBoard(board):
    return [row[:] for row in board]

# Hàm kiểm tra nước đi hợp lệ
def checkValidMove(board, pace):
    
    return True

# Hàm trả về một list các tuple [(a,b),(b,c),...], là tập các vị trí quân cờ đối thủ bị ăn khi đi nước đi pace.
def carryPoint(board, pace):
    return

def select_move(cur_state, player_to_move, remain_time):
    return