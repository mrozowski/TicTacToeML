from PyQt5 import QtCore, QtGui, QtWidgets
import button


class View(object):
    def __init__(self):
        self.board = []
        self.presenter = None
        self.btn_new_game = None
        self.circle_score = None
        self.cross_score = None
        self.games_label = None
        self.btn_computers = None
        self.btn_training = None
        self.btn_exit = None
        self.statusbar = None

    def set_presenter(self, presenter):
        self.presenter = presenter

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 371)
        MainWindow.resize(600, 371)
        MainWindow.setStyleSheet("background-color: #131313;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("color: white;")
        self.centralwidget.setObjectName("centralwidget")
        self.board_bg = QtWidgets.QLabel(self.centralwidget)
        self.board_bg.setGeometry(QtCore.QRect(15, 15, 320, 320))
        self.board_bg.setText("")
        self.board_bg.setPixmap(QtGui.QPixmap("graphic/board.png"))
        self.board_bg.setScaledContents(False)
        self.board_bg.setObjectName("board_bg")
        self.score_bg = QtWidgets.QLabel(self.centralwidget)
        self.score_bg.setGeometry(QtCore.QRect(348, 15, 238, 100))
        self.score_bg.setText("")
        self.score_bg.setPixmap(QtGui.QPixmap("graphic/score_bg.png"))
        self.score_bg.setObjectName("score_bg")

        self.btn_new_game = button.PicButton("New Game", self.centralwidget)
        self.btn_new_game.setGeometry(QtCore.QRect(348, 124, 148, 52))
        self.btn_new_game.setObjectName("button_label1")
        self.btn_new_game.clicked.connect(lambda: self.presenter.new_game())

        self.btn_computers = button.PicButton("Comp vs comp", self.centralwidget)
        self.btn_computers.setGeometry(QtCore.QRect(348, 180, 148, 52))
        self.btn_computers.setObjectName("button_label2")
        self.btn_computers.clicked.connect(lambda: self.presenter.comp_vs_comp())

        self.btn_training = button.PicButton("Trening", self.centralwidget)
        self.btn_training.setGeometry(QtCore.QRect(348, 236, 148, 52))
        self.btn_training.setObjectName("button_label3")
        self.btn_training.clicked.connect(lambda: self.presenter.training())

        self.btn_exit = button.PicButton("Exit", self.centralwidget)
        self.btn_exit.setGeometry(QtCore.QRect(348, 292, 148, 52))
        self.btn_exit.setObjectName("button_label4")
        self.btn_exit.clicked.connect(lambda: self.presenter.exit())

        self.player1 = QtWidgets.QLabel(self.centralwidget)
        self.player1.setGeometry(QtCore.QRect(520, 128, 55, 16))
        self.player1.setObjectName("player1")

        self.player2 = QtWidgets.QLabel(self.centralwidget)
        self.player2.setGeometry(QtCore.QRect(520, 219, 55, 16))
        self.player2.setObjectName("player2")

        self.circle_label = QtWidgets.QLabel(self.centralwidget)
        self.circle_label.setGeometry(QtCore.QRect(525, 155, 30, 30))
        self.circle_label.setText("")
        self.circle_label.setPixmap(QtGui.QPixmap("graphic/circle.png"))
        self.circle_label.setScaledContents(True)
        self.circle_label.setObjectName("circle_label")
        self.circle_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.circle_label.mousePressEvent = self.presenter.change_to_circle

        self.cross_label = QtWidgets.QLabel(self.centralwidget)
        self.cross_label.setGeometry(QtCore.QRect(525, 245, 30, 30))
        self.cross_label.setText("")
        self.cross_label.setPixmap(QtGui.QPixmap("graphic/cross.png"))
        self.cross_label.setScaledContents(True)
        self.cross_label.setObjectName("cross_label")
        self.cross_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cross_label.mousePressEvent = self.presenter.change_to_cross

        gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 311, 311))
        gridLayoutWidget.setObjectName("gridLayoutWidget")
        gridLayoutWidget.setStyleSheet("background-color: transparent;")

        self.board_grid = QtWidgets.QGridLayout(gridLayoutWidget)
        self.board_grid.setContentsMargins(5, 5, 5, 5)
        self.board_grid.setSpacing(20)
        self.board_grid.setObjectName("board_grid")

        b20 = button.NodeBoard(gridLayoutWidget)
        b20.setObjectName("b20")
        self.board_grid.addWidget(b20, 5, 2, 1, 1)

        b01 = button.NodeBoard(gridLayoutWidget)
        b01.setObjectName("b01")
        self.board_grid.addWidget(b01, 3, 3, 1, 1)

        b10 = button.NodeBoard(gridLayoutWidget)
        b10.setObjectName("b10")
        self.board_grid.addWidget(b10, 4, 2, 1, 1)

        b00 = button.NodeBoard(gridLayoutWidget)
        b00.setObjectName("b00")
        self.board_grid.addWidget(b00, 3, 2, 1, 1)

        b21 = button.NodeBoard(gridLayoutWidget)
        b21.setObjectName("b21")
        self.board_grid.addWidget(b21, 5, 3, 1, 1)

        b12 = button.NodeBoard(gridLayoutWidget)
        b12.setObjectName("b12")
        self.board_grid.addWidget(b12, 4, 4, 1, 1)

        b11 = button.NodeBoard(gridLayoutWidget)
        b11.setObjectName("b11")
        self.board_grid.addWidget(b11, 4, 3, 1, 1)

        b22 = button.NodeBoard(gridLayoutWidget)
        b22.setObjectName("b22")
        self.board_grid.addWidget(b22, 5, 4, 1, 1)

        b02 = button.NodeBoard(gridLayoutWidget)
        b02.setObjectName("b02")
        self.board_grid.addWidget(b02, 3, 4, 1, 1)

        b00.clicked.connect(lambda: self.presenter.action(0))
        b01.clicked.connect(lambda: self.presenter.action(1))
        b02.clicked.connect(lambda: self.presenter.action(2))
        b10.clicked.connect(lambda: self.presenter.action(3))
        b11.clicked.connect(lambda: self.presenter.action(4))
        b12.clicked.connect(lambda: self.presenter.action(5))
        b20.clicked.connect(lambda: self.presenter.action(6))
        b21.clicked.connect(lambda: self.presenter.action(7))
        b22.clicked.connect(lambda: self.presenter.action(8))

        self.board.append(b00)
        self.board.append(b01)
        self.board.append(b02)
        self.board.append(b10)
        self.board.append(b11)
        self.board.append(b12)
        self.board.append(b20)
        self.board.append(b21)
        self.board.append(b22)

        self.circle_score = QtWidgets.QLabel(self.centralwidget)
        self.circle_score.setGeometry(QtCore.QRect(430, 55, 55, 16))
        self.circle_score.setStyleSheet("background-color: transparent;")
        self.circle_score.setAlignment(QtCore.Qt.AlignCenter)
        self.circle_score.setObjectName("circle_score")

        self.cross_score = QtWidgets.QLabel(self.centralwidget)
        self.cross_score.setGeometry(QtCore.QRect(430, 80, 55, 16))
        self.cross_score.setStyleSheet("background-color: transparent;")
        self.cross_score.setAlignment(QtCore.Qt.AlignCenter)
        self.cross_score.setObjectName("cross_score")

        self.games_label = QtWidgets.QLabel(self.centralwidget)
        self.games_label.setGeometry(QtCore.QRect(500, 60, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.games_label.setFont(font)
        self.games_label.setStyleSheet("background-color: transparent;")
        self.games_label.setAlignment(QtCore.Qt.AlignCenter)
        self.games_label.setObjectName("games_label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("color: white;")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TicTacToeML"))
        self.player1.setText(_translate("MainWindow", "Player 1"))
        self.player2.setText(_translate("MainWindow", "Player 2"))
        self.circle_score.setText(_translate("MainWindow", "0"))
        self.cross_score.setText(_translate("MainWindow", "0"))
        self.games_label.setText(_translate("MainWindow", "0"))




