from const import BOARD_COLS, BOARD_ROWS
import numpy as np
import time

class Machine:
    def __init__(self, p1, p2, show_move, show_winner_nodes, update_score):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.p1 = p1
        self.p2 = p2
        self.isEnd = False
        self.boardHash = None
        self.show_move = show_move
        self.show_winner_nodes = show_winner_nodes
        self.update_score = update_score
        self.isReset = False

    # get unique hash of current board state
    def get_hash(self):
        self.boardHash = str(self.board.reshape(BOARD_COLS * BOARD_ROWS))
        return self.boardHash

    def winner(self):
        # row
        for i in range(BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1, 0, i
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1, 0, i
        # col
        for i in range(BOARD_COLS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1, 1, i
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1, 1, i
        # diagonal
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3:
                return 1,  2, 0
            elif diag_sum1 == -3:
                return -1, 2, 0
            elif diag_sum2 == 3:
                return 1,  3, 0
            elif diag_sum2 == -3:
                return -1, 3, 0

        # tie - no available positions
        if len(self.available_positions()) == 0:
            self.isEnd = True
            return [0, 0, 0]
        # not end
        self.isEnd = False
        return [None, None, None]

    def available_positions(self):
        positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def update_state(self, position, symbol):
        self.board[position] = symbol
        self.show_move(position, symbol)

    def give_reward(self):
        result = self.winner()[0]
        # backpropagate reward
        if result == 1:
            self.p1.feed_reward(1)
            self.p2.feed_reward(0)
        elif result == -1:
            self.p1.feed_reward(0)
            self.p2.feed_reward(1)
        else:
            self.p1.feed_reward(0.5)
            self.p2.feed_reward(0.5)

    def reset(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.boardHash = None
        self.isEnd = False

    def play(self, rounds=100):
        for i in range(rounds):
            while not self.isEnd:
                # Player 1
                positions = self.available_positions()
                p1_action = self.p1.make_move(positions, self.board)

                # take action and update board state
                self.board[p1_action] = self.p1.symbol

                board_hash = self.get_hash()
                self.p1.add_state(board_hash)
                # check board status if it is end

                win = self.winner()[0]
                if win is not None:
                    # self.showBoard()
                    # ended with p1 either win or draw
                    self.give_reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.update_score(win)
                    self.reset()
                    break

                else:
                    # Player 2
                    positions = self.available_positions()
                    p2_action = self.p2.make_move(positions, self.board)

                    self.board[p2_action] = self.p2.symbol

                    board_hash = self.get_hash()
                    self.p2.add_state(board_hash)

                    win = self.winner()[0]
                    if win is not None:
                        # self.showBoard()
                        # ended with p2 either win or draw
                        self.give_reward()
                        self.p1.reset()
                        self.p2.reset()
                        self.update_score(win)
                        self.reset()
                        break

    def play2(self):
        """Computer vs Human """
        self.isReset = False
        while not self.isEnd:
            if self.isReset:  # if someone click new game before finish match it will end this method
                return

            # Player 1 turn  - Computer
            positions = self.available_positions()
            p1_action = self.p1.make_move(positions, self.board)
            self.update_state(p1_action, self.p1.symbol)

            if self.check_win():
                break
            else:
                # Player 2 turn - Human
                positions = self.available_positions()
                p2_action = self.p2.make_move(positions)

                self.update_state(p2_action, self.p2.symbol)

                if self.check_win():
                    break

    def play3(self):
        """Computer vs Computer"""
        self.isReset = False
        while not self.isEnd:
            if self.isReset:  # if someone click new game before finish match it will end this method
                return

            # Player 1 turn
            positions = self.available_positions()
            p1_action = self.p1.make_move(positions, self.board)
            self.update_state(p1_action, self.p1.symbol)
            time.sleep(0.5)  # wait half second before next move

            if self.check_win():
                break
            else:
                # Player 2 turn
                positions = self.available_positions()
                p2_action = self.p2.make_move(positions, self.board)
                self.update_state(p2_action, self.p2.symbol)
                time.sleep(0.5)

                if self.check_win():
                    break

    def play4(self):
        """Human vs Computer"""
        self.isReset = False
        while not self.isEnd:
            if self.isReset:  # if someone click new game before finish match it will end this method
                return

            # Player 1 turn - Human
            positions = self.available_positions()
            p2_action = self.p2.make_move(positions)
            self.update_state(p2_action, self.p2.symbol)

            if self.check_win():
                break
            else:
                # Player 2 turn - Computer
                positions = self.available_positions()
                p1_action = self.p1.make_move(positions, self.board)

                self.update_state(p1_action, self.p1.symbol)

                if self.check_win():
                    break

    def check_win(self):
        win, where, pos = self.winner()
        if win is not None:
            if win != 0:
                self.show_winner_nodes(where, pos)
            self.update_score(win)
            self.reset()
            return True
        return False

    def set_end(self):
        self.isEnd = True
        self.isReset = True




