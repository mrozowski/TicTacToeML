from PyQt5 import QtWidgets, QtGui
from game import Machine
from player import Player, HumanPlayer
import sys
import threading
import const
import view

class Presenter:
    def __init__(self, _view: view.View):
        self.view = _view
        self.games = 0
        self.player2 = HumanPlayer("p2", -1)
        self.player1 = Player("pl", 1)
        self.player1.loadPolicy("policy/policy_p1")
        self.computer = 1
        self.machine = None
        self.game_type = ""
        self.disabled_action = True  # disable ability to click on board
        self.t = None

    def setup(self):
        self.view.statusbar.showMessage(self.game_type)
        self.machine = Machine(self.player1,
                               self.player2,
                               self.computer_action,
                               self.show_winner_nodes,
                               self.update_score)

    def new_game(self):
        if threading.active_count() > 1:  # it prevents from clicking many times button 'new game'
            return                        # and creating too many useless threads

        self.game_type = const.GAME_TYPE_1
        self.disabled_action = False
        if isinstance(self.player2, Player):
            self.player2 = HumanPlayer("p2", -1)

        if self.t is not None and self.t.stopped() is False:
            self.t.stop()
        self.clean_board()
        self.setup()

        self.t = StoppableThread(target=self.start_human_vs_comp, reset=self.machine.set_end)
        self.t.daemon = True  # kill this thread when main thread is killed
        self.t.start()

    def comp_vs_comp(self):
        if threading.active_count() > 1:
            return

        self.game_type = const.GAME_TYPE_2
        self.disabled_action = True
        if isinstance(self.player2, HumanPlayer):
            self.player2 = Player("p2", -1)
            self.player2.loadPolicy("policy/policy_p2")

        self.clean_board()
        if self.t is not None and self.t.stopped() is False:
            self.t.stop()

        self.setup()

        self.t = StoppableThread(target=self.start_comp_vs_comp, reset=self.machine.set_end)
        self.t.daemon = True  # kill this thread when main thread is killed
        self.t.start()

    def training(self):
        if self.game_type == const.GAME_TYPE_3:
            return

        self.game_type = const.GAME_TYPE_3
        self.disabled_action = True
        self.player2 = Player("p_training2", -1)
        self.player1 = Player("p_training1", 1)
        self.clean_board()
        self.reset_score()

        if self.t is not None and self.t.stopped() is False:
            self.t.stop()
        self.setup()

        self.t = StoppableThread(target=self.start_training, reset=self.machine.set_end)
        self.t.daemon = True
        self.t.start()

    def start_training(self):
        self.machine.play(5000)
        self.player1.savePolicy()
        self.player2.savePolicy()
        self.new_game()

    def start_human_vs_comp(self):
        self.machine.play2()

    def start_comp_vs_comp(self):
        self.machine.play3()

    def show_winner_nodes(self, switch: int, pos: int = 0):
        if switch == 0:    # row
            for i in range(3):
                self.view.board[pos * 3 + i].mark_as_winner()
        elif switch == 1:  # column
            for i in range(3):
                self.view.board[i * 3 + pos].mark_as_winner()
        elif switch == 2:  # diagonal \
            for i in range(3):
                self.view.board[i * 4].mark_as_winner()
        elif switch == 3:  # diagonal /
            for i in range(3):
                self.view.board[(i + 1) * 2].mark_as_winner()

    def show(self):
        app = QtWidgets.QApplication(sys.argv)
        app.setWindowIcon(QtGui.QIcon('graphic/icon.ico'))
        MainWindow = QtWidgets.QMainWindow()
        self.view.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

    def update_score(self, winner):
        self.disabled_action = True  # disable ability to click on board after match is finished
        if self.player2.symbol == 1:
            nought = self.player2
            cross = self.player1
        else:
            cross = self.player2
            nought = self.player1

        if winner == 1:
            nought.score += 1
            self.view.circle_score.setText(str(nought.score))
            self.view.statusbar.showMessage("Nought win!")
        elif winner == -1:
            cross.score += 1
            self.view.cross_score.setText(str(cross.score))
            self.view.statusbar.showMessage("Cross win!")
        else:
            self.view.statusbar.showMessage("Tie!")
        self.games += 1
        self.view.games_label.setText(str(self.games))

    def computer_action(self, action, symbol: int):
        a = int(action[0])
        b = int(action[1])

        index = a * 3 + b
        self.view.board[index].action(symbol)

    def action(self, i_node: int):
        if self.disabled_action:
            return
        self.view.board[i_node].action(self.player2.symbol)
        self.player2.click(i_node)

    def clean_board(self):
        for node in self.view.board:
            node.reset()

    def reset_score(self):
        self.view.circle_score.setText("0")
        self.view.cross_score.setText("0")
        self.games = 0
        self.view.games_label.setText(str(self.games))

    def exit(self):
        exit()


class StoppableThread(threading.Thread):
    def __init__(self,  target, reset):
        super(StoppableThread, self).__init__(target=target)
        self._stop_event = threading.Event()
        self.reset = reset

    def stop(self):
        self.reset()
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()



