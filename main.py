from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys
from pygame import mixer, mixer_music
import qtawesome as qta


class MusicApp(QWidget):
    def __init__(self):
        super().__init__()

        # Title
        self.setWindowTitle("boop")
        self.setFixedWidth(800)
        self.setFixedHeight(400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet(
            """
            * {background: #111;}
            QPushButton { 
            background: '#f0f0f0';
            border-radius: 20px;
            min-width: 40px;
            height: 40px;
            button-layout: 1;
            }
            QPushButton:hover {
            background: white;
            }
            QPushButton:pressed {
            background: '#f0f0f0';
            }
            
            QLabel {
            color: white;
            }
            """)
        # Title
        self.title = QLabel('.wav Music Player', self)
        self.title.move(20, 26)

        # Play button
        self.btn_play_pause = QPushButton('', self)
        self.btn_play_pause.setIcon(QIcon('images/play-fill.png'))
        self.btn_play_pause.setIconSize(QtCore.QSize(30, 30))
        self.btn_play_pause.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_play_pause.clicked.connect(self.play_pause)
        self.btn_play_pause.move(380, 320)

        # Exit button
        self.icon_exit = qta.icon('mdi.close', color='#ffffff', color_selected='#ffffff', scale_factor=2)
        self.btn_exit = QPushButton(self.icon_exit, '', self)
        self.btn_exit.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_exit.clicked.connect(exit)
        self.btn_exit.setStyleSheet("background: '#111';")
        self.btn_exit.move(750, 10)

        self.old_pos = self.pos()

        self.show()

    def play_pause(self):
        mixer.init()
        if mixer_music.get_busy() == 0:

            self.btn_play_pause.setIcon(QIcon('images/pause-fill.png'))
            if mixer_music.get_pos() != -1:
                mixer_music.unpause()
            else:
                mixer_music.load('[ONTIVA.COM] The Rabbit That Hunts Tigers-HQ.wav')
                mixer_music.play()

        elif mixer_music.get_busy() == 1:
            self.btn_play_pause.setIcon(QIcon('images/play-fill.png'))
            mixer_music.pause()

    def stop(self):
        mixer_music.stop()
        self.btn_play_pause.setIcon(QIcon('images/play-fill.png'))

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        moved = QtCore.QPoint(event.globalPos() - self.old_pos)
        self.move(self.x() + moved.x(), self.y() + moved.y())
        self.old_pos = event.globalPos()


app = QApplication(sys.argv)
root = MusicApp()

app.exec()
