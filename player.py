import pickle

import numpy as np
from const import BOARD_COLS, BOARD_ROWS

class Player:
    def __init__(self, name, symbol, exp_rate=0.15):
        self.name = name
        self.symbol = symbol
        self.score = 0
        self.states = []  # record all positions taken
        self.lr = 0.1
        self.exp_rate = exp_rate
        self.decay_rate = 0.9
        self.states_value = {}  # state -> value

    def get_hash(self, board):
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash

    def make_move(self, positions, current_board):
        if np.random.random() <= self.exp_rate:
            # make a random decision
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            # calculate the best move
            value_max = -100
            for p in positions:
                # check all available moves
                next_board = current_board.copy()
                next_board[p] = self.symbol
                next_board_hash = self.get_hash(next_board)

                temp = self.states_value.get(next_board_hash)
                value = 0
                if temp is not None: value = temp
                if value >= value_max:
                    value_max = value
                    action = p
        return action

    # append a hash state
    def add_state(self, state):
        self.states.append(state)

    def feed_reward(self, reward):
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            self.states_value[state] += self.lr * (self.decay_rate * reward - self.states_value[state])
            reward = self.states_value[state]

    def reset(self):
        self.states = []

    def save_policy(self):
        fw = open('policy/policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def load_policy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.score = 0
        self.ready = False
        self.action = None

    def make_move(self, positions):
        while True:
            if self.ready:
                if self.action in positions:
                    self.ready = False
                    return self.action
                else:
                    self.ready = False

    def click(self, index: int):
        a = int(index / 3)
        b = a * (-3) + index
        self.action = a, b
        self.ready = True
