import pickle

import numpy as np
from const import BOARD_COLS, BOARD_ROWS

class Player:
    def __init__(self, name, symbol, exp_rate=0.15):
        self.name = name
        self.symbol = symbol
        self.score = 0
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value

    def getHash(self, board):
        boardHash = str(board.reshape(BOARD_COLS * BOARD_ROWS))
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        if np.random.random() <= self.exp_rate:
            # take random action
            idx = np.random.choice(len(positions))
            action = positions[idx]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                # print("value", value)
                if value >= value_max:
                    value_max = value
                    action = p
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy/policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
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

    def chooseAction(self, positions):
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
