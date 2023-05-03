import pygame as pg
import numpy as np
import time
from Agents import Agents
import Minimax as minimax
from enum import Enum


BG_COLOR = (255, 221, 192)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (59,  163, 6)
BOARD_SIZE = 8
DELAY_TIME = 6
TOTAL_TIME = 60
LIMIT_TIME = 8
INITIAL_STATE = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, -1, 0, 0, 0],
                 [0, 0, 0, -1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]]

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

FONT_SIZE = 32

MARGIN = 50
CELL_SIZE = 60

class ManualPlayer(Enum):
    NO_PLAYER = 0
    PLAYER_1 = 1
    PLAYER_2 = 2


def main():
    # self = input("Nhap 1 neu di truoc, 2 neu di sau: ")
    # PLAYER_1, PLAYER_2 = None, None
    # # Mình quân trắng đi trước
    # if self == "1":
    #     PLAYER_1 = Player(minimax.select_move,"SELF", 1)
    #     PLAYER_2 = Player(ag.random_agent,"OPPONENT", -1)
    # # Mình quân đen đi sau
    # elif self == "2":
    #     PLAYER_1 = Player(ag.random_agent,"OPPONENT",1)
    #     PLAYER_2 = Player(minimax.select_move,"SELF", -1)

    board = Board(INITIAL_STATE)
    # player1 = PLAYER_1
    # player2 = PLAYER_2
    # chọn AGENT MÀ MÌNH MUỐN
    game = Game(board=board)
    game.loop()


class Board:
    def __init__(self, board_state):
        self.board_state = board_state

    def draw_board(self, surface):
        surface.fill(BG_COLOR)

        for i in range(1, BOARD_SIZE):
            x = i * CELL_SIZE
            pg.draw.line(surface, BLACK_COLOR, (x, 0), (x, 480), 2)
            pg.draw.line(surface, BLACK_COLOR, (0, x), (480, x), 2)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board_state[row][col] == 1:
                    pg.draw.circle(surface, WHITE_COLOR,
                                   (col * CELL_SIZE + 30, row * CELL_SIZE + 30), 25)
                elif self.board_state[row][col] == -1:
                    pg.draw.circle(surface, BLACK_COLOR,
                                   (col * CELL_SIZE + 30, row * CELL_SIZE + 30), 25)
    
    def is_valid_move(self, board, row, col, turn):
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
                    if board[r][c] == turn:
                        if found_opponent:
                            return True
                        break
                    found_opponent = True
                    r += i
                    c += j
        return False

    def get_valid_moves(self, board, turn):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(board, row, col, turn):
                    valid_moves.append((row, col))
        return valid_moves

    def update_board(self, position, player):
        def make_move(board, row, col, turn):
            new_board = [row[:] for row in board]

            new_board[row][col] = turn

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue

                    r = row + i
                    c = col + j
                    flipped = False
                    to_flip = []

                    while r >= 0 and r < 8 and c >= 0 and c < 8:
                        if new_board[r][c] == 0:
                            break
                        if new_board[r][c] == turn:
                            flipped = True
                            break
                        to_flip.append((r, c))
                        r += i
                        c += j

                    if flipped:
                        for (r, c) in to_flip:
                            new_board[r][c] = turn

            return new_board
        valid_move = self.get_valid_moves(self.board_state, player)
        if valid_move == []:
            valid_move.append(None)
        if position not in valid_move:
            return False
        if position == None:
            return True
        (x, y) = position
        self.board_state = make_move(self.board_state, x, y, player)
        return True

    def get_board(self):
        return self.board_state
    
    # highlights valid moves
    def highlight_valid_moves(self, surface, valid_moves):
        for move in valid_moves:
            row, col = move
            pg.draw.circle(surface, GREEN_COLOR, (col * 60 + 30, row * 60 + 30), 25, 5)
            pg.display.flip()

class Player:
    def __init__(self, agent, name, turn) -> None:
        self.agent = agent
        self.name = name
        self.turn = turn
        self.time = TOTAL_TIME
        self.last_move = None

    def move(self, board_state):
        start_time = time.perf_counter()
        ans = self.agent(board_state, self.turn, self.time)
        elapsed_time = time.perf_counter() - start_time
        if elapsed_time > LIMIT_TIME:
            return -1
        self.time -= elapsed_time
        if elapsed_time < 0:
            return -1
        self.last_move = ans
        return ans


class Game:
    def __init__(self, board: Board):
        pg.init()
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.board = board
        self.player1 = None
        self.player2 = None

        # For manual mode
        self.is_manual_mode = False
        self.manual_player = ManualPlayer.NO_PLAYER

        clock = pg.time.Clock()

        player = None

        while not player:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        player = "1"
                    elif event.key == pg.K_2:
                        player = "2"
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos
                        if self.exit_button_rect.collidepoint(mouse_pos):
                            pg.quit()
                            return

            self.draw_menu(self.screen)
            clock.tick(60)

        # Start the game with selected player

        # instance of agent: random agent and manual agent
        agent = Agents()

        # if player == "1":
        #     print("Player 1 selected")
        #     self.player1 = Player(minimax.select_move,"SELF", 1)
        #     self.player2 = Player(agent.random_agent,"OPPONENT", -1)
        # elif player == "2":
        #     print("Player 2 selected")
        #     self.player1 = Player(agent.random_agent,"OPPONENT", 1)
        #     self.player2 = Player(minimax.select_move,"SELF",-1)

        if player == "1":
            print("Select white, move first")
            self.player1 = Player(agent.manual_agent, "SELF", 1)
            self.player2 = Player(minimax.select_move, "OPPONENT", -1)
            self.is_manual_mode = True
            self.manual_player = ManualPlayer.PLAYER_1

        elif player == "2":
            print("Select black, move second")
            self.player1 = Player(minimax.select_move, "OPPONENT", 1)
            self.player2 = Player(agent.manual_agent, "SELF", -1)
            self.is_manual_mode = True
            self.manual_player = ManualPlayer.PLAYER_2

    def draw_text(self, surface, text, x, y):
        font = pg.font.Font(None, FONT_SIZE)
        text_surface = font.render(text, True, BLACK_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def draw_menu(self, surface):
        surface.fill(BG_COLOR)
        self.draw_text(surface, "Choose your player",
                       WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
        self.draw_text(surface, "Press 1 to choose Player 1",
                       WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.draw_text(surface, "Press 2 to choose Player 1",
                       WINDOW_WIDTH/2, WINDOW_HEIGHT*3/4)
        # Draw exit button
        self.exit_button_rect = pg.Rect(WINDOW_WIDTH-80, 20, 60, 30)
        pg.draw.rect(surface, WHITE_COLOR, self.exit_button_rect)
        self.draw_text(surface, "Exit", WINDOW_WIDTH-50, 35)
        pg.display.update()

    def end_check(self):
        curr_board = self.board.get_board()
        # null=player1=player2 = 0
        # for i in curr_board:
        #     if 0 in i: null+=1
        #     if 1 in i: player1+=1
        #     if -1 in i: player2+=1
        # return null==0 or player1==0 or player2==0

        def is_valid_move(board, row, col, turn):
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
                        if board[r][c] == turn:
                            if found_opponent:
                                return True
                            break
                        found_opponent = True
                        r += i
                        c += j
            return False

        def get_valid_moves(board, turn):
            valid_moves = []
            for row in range(8):
                for col in range(8):
                    if is_valid_move(board, row, col, turn):
                        valid_moves.append((row, col))
            return valid_moves
        return get_valid_moves(curr_board, 1) == [] and get_valid_moves(curr_board, -1) == []

    def win_check(self):
        curr_board = self.board.get_board()
        player1 = 0
        player2 = 0
        for i in curr_board:
            for j in i:
                if j == 1:
                    player1 += 1
                elif j == -1:
                    player2 += 1
        if player1 > player2:
            return 1
        if player2 > player1:
            return -1
        return 0

    def draw_turn(self, player1, player2, playerturn):
        font = pg.font.Font(None, 30)
        player1_name = font.render(player1.name, True, BLACK_COLOR)
        player2_name = font.render(player2.name, True, BLACK_COLOR)
        player1_last_move = font.render(
            "Last Move: "+str(player1.last_move), True, BLACK_COLOR)
        player2_last_move = font.render(
            "Last Move: "+str(player2.last_move), True, BLACK_COLOR)
        player1_time = font.render(
            f"Time left: {player1.time:.5f}s", True, BLACK_COLOR)
        player2_time = font.render(
            f"Time left: {player2.time:.5f}s", True, BLACK_COLOR)
        player1_name_rect = player1_name.get_rect()
        player2_name_rect = player2_name.get_rect()
        player1_last_move_rect = player1_last_move.get_rect()
        player2_last_move_rect = player2_last_move.get_rect()
        player1_time_rect = player1_time.get_rect()
        player2_time_rect = player2_time.get_rect()
        player1_name_rect.center = (WINDOW_WIDTH - 200, 50)
        player2_name_rect.center = (WINDOW_WIDTH - 200, WINDOW_HEIGHT/2)
        player1_last_move_rect.center = (WINDOW_WIDTH - 100, 100)
        player2_last_move_rect.center = (
            WINDOW_WIDTH - 100, WINDOW_HEIGHT/2+50)
        player1_time_rect.center = (WINDOW_WIDTH - 100, 150)
        player2_time_rect.center = (WINDOW_WIDTH - 100, WINDOW_HEIGHT/2+100)
        if playerturn == 1:
            player1_name = font.render(player1.name+"'s Turn", True, RED_COLOR)
        else:
            player2_name = font.render(player2.name+"'s Turn", True, RED_COLOR)
        self.screen.blit(player1_name, player1_name_rect)
        self.screen.blit(player2_name, player2_name_rect)
        self.screen.blit(player1_last_move, player1_last_move_rect)
        self.screen.blit(player2_last_move, player2_last_move_rect)
        self.screen.blit(player1_time, player1_time_rect)
        self.screen.blit(player2_time, player2_time_rect)

    def print_message(self, reason):
        font = pg.font.Font(None, 30)
        text = font.render(reason, True, RED_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (WINDOW_WIDTH-300, WINDOW_HEIGHT-100)
        self.screen.blit(text, text_rect)

    def loop(self):
        turn = 1
        self.board.draw_board(self.screen)
        self.draw_turn(self.player1, self.player2, turn)
        pg.display.flip()
        looping = False
        winner = 0
        move = None
        while not looping:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    looping = False
            if turn == 1:
                if (self.is_manual_mode):
                    if (self.manual_player == ManualPlayer.PLAYER_1):
                        valid_moves = self.board.get_valid_moves(self.board.board_state, turn)
                        self.board.highlight_valid_moves(self.screen, valid_moves)
                        print("Valid moves 1: ", valid_moves)

                move = self.player1.move(self.board.board_state)
                if move == -1:
                    winner = -1
                    self.print_message(self.player1.name +
                                       " lose due to out of time")
                    open('Output.txt', mode='a', encoding='utf-8').writelines(
                        self.player1.name+" lose due to out of time" + '\n')
                    pg.display.flip()
                    time.sleep(DELAY_TIME)
                    break
            else:
                if (self.is_manual_mode):
                    if (self.manual_player == ManualPlayer.PLAYER_2):
                        valid_moves =  self.board.get_valid_moves(self.board.board_state, turn)
                        self.board.highlight_valid_moves(self.screen, valid_moves)
                        print("Valid moves 2: ", valid_moves)

                move = self.player2.move(self.board.board_state)
                if move == -1:
                    winner = 1
                    self.print_message(self.player2.name +
                                       " lose due to out of time")
                    open('Output.txt', mode='a', encoding='utf-8').writelines(
                        self.player2.name+" lose due to out of time" + '\n')
                    pg.display.flip()
                    time.sleep(DELAY_TIME)
                    break
            valid_move = self.board.update_board(move, turn)
            if not valid_move:
                if turn == 1:
                    winner = -1
                    self.print_message(self.player1.name +
                                       " lose due to invalid move")
                    open('Output.txt', mode='a', encoding='utf-8').writelines(
                        self.player1.name+" lose due to invalid move" + '\n')
                    pg.display.flip()
                    time.sleep(DELAY_TIME)
                    break
                else:
                    winner = 1
                    self.print_message(self.player2.name +
                                       " lose due to invalid move")
                    open('Output.txt', mode='a', encoding='utf-8').writelines(
                        self.player2.name+" lose due to invalid move" + '\n')
                    pg.display.flip()
                    time.sleep(DELAY_TIME)
                    break

            self.board.draw_board(self.screen)
            self.draw_turn(self.player1, self.player2, turn)
            pg.display.flip()
            time.sleep(2)
            if turn == 1:
                open('move.txt', mode='a',
                     encoding='utf-8').writelines("Player 1 move: "+str(move)+'\n')
            else:
                open('move.txt', mode='a',
                     encoding='utf-8').writelines("Player 2 move: "+str(move)+'\n')
            looping = self.end_check()
            if looping:
                winner = self.win_check()
            else:
                turn = - turn
        print(winner)
        if winner == 1:
            winner = self.player1.name + " win"
        elif winner == -1:
            winner = self.player2.name + " win"
        else:
            winner = self.player1.name + " draw " + self.player2.name
        self.board.draw_board(self.screen)
        self.print_message(winner)
        open('Output.txt', mode='a', encoding='utf-8').writelines(winner + '\n \n')
        open('move.txt', mode='a', encoding='utf-8').writelines('\n')
        pg.display.flip()
        time.sleep(DELAY_TIME*1.5)
        input("Press any key to exit...")


if __name__ == "__main__":
    main()
