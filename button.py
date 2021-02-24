from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractButton, QPushButton


class PicButton(QAbstractButton):
    """Custom buttons"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.pixmap = QtGui.QPixmap("graphic/button.png")
        self.pixmap_hover = QtGui.QPixmap("graphic/button_hover.png")
        self.pixmap_pressed = QtGui.QPixmap("graphic/button_pressed.png")
        self.setStyleSheet("color: #5CDBD3; font-size: 10pt;")
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def paintEvent(self, event):
        """show the button"""
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)  # draw button
        painter.drawText(QRectF(0, -3.5, self.width(), self.height()), Qt.AlignCenter, self.text)  # draw text in the center of button


class NodeBoard(QPushButton):
    """Custom buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QtCore.QSize(70, 70))
        self.setFixedHeight(70)

        self.setStyleSheet("background-color: transparent;")
        self.setText("")
        self.set = 0

    def action(self, player: int):
        if self.set != 0: return
        player_icon = None
        if player == 1:
            player_icon = QtGui.QIcon("graphic/circle.png")
        elif player == -1:
            player_icon = QtGui.QIcon("graphic/cross.png")

        self.setIcon(player_icon)
        self.set = player

    def reset(self):
        self.set = 0
        self.setIcon(QtGui.QIcon())

    def mark_as_winner(self):
        player_icon = None
        if self.set == 1:
            player_icon = QtGui.QIcon("graphic/circlewin.png")
        elif self.set == -1:
            player_icon = QtGui.QIcon("graphic/crosswin.png")

        self.setIcon(player_icon)



