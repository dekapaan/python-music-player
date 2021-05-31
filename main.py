from PyQt5.QtWidgets import *
import os
from PyQt5.QtGui import *
from PyQt5 import QtCore
import sys
from pygame import mixer, mixer_music
import qtawesome as qta
from tinytag import TinyTag


class MusicApp(QWidget):
    def __init__(self):

        super().__init__()
        self.setFixedWidth(800)
        self.setFixedHeight(400)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
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

            QListWidget {
            background: #1e1e1e;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            }

            QPixmap {
            min-width: 20px;
            }
            """)
        # Title
        self.title = QLabel('.wav Music Player', self)
        self.title.move(20, 26)

        # Play button
        self.btn_play_pause = QPushButton('', self)
        self.btn_play_pause.setIcon(QIcon('images/play-fill.png'))
        self.btn_play_pause.setIconSize(QtCore.QSize(30, 30))
        self.btn_play_pause.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_play_pause.clicked.connect(self.play_pause)
        self.btn_play_pause.move(390, 325)

        # Exit button
        self.icon_exit = qta.icon('mdi.close', color='#ffffff', color_selected='#ffffff', scale_factor=2)
        self.btn_exit = QPushButton(self.icon_exit, '', self)
        self.btn_exit.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_exit.clicked.connect(exit)
        self.btn_exit.setStyleSheet("background: '#111';")
        self.btn_exit.move(750, 10)

        self.icon_minimize = qta.icon('mdi.window-minimize', color='#ffffff', scale_factor=2)
        self.btn_minimize = QPushButton(self.icon_minimize, '', self)
        self.btn_minimize.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_minimize.clicked.connect(self.showMinimized)
        self.btn_minimize.setStyleSheet("background: '#111';")
        self.btn_minimize.move(710, 13)

        self.icon_rewind = qta.icon('mdi.skip-previous', color='#ffffff', scale_factor=2)
        self.btn_rewind = QPushButton(self.icon_rewind, '', self)
        self.btn_rewind.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_rewind.clicked.connect(self.rewind)
        self.btn_rewind.setStyleSheet("background: #111;")
        self.btn_rewind.move(340, 324)

        self.icon_forward = qta.icon('mdi.skip-next', color='#ffffff', scale_factor=2)
        self.btn_forward = QPushButton(self.icon_forward, '', self)
        self.btn_forward.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.btn_forward.clicked.connect(self.skip)
        self.btn_forward.setStyleSheet("background: #111;")
        self.btn_forward.move(440, 324)

        self.playlist = QListWidget(self)
        self.playlist.setFixedWidth(400)
        self.playlist.move(203, 70)
        self.playlist_list = []
        for i in os.listdir('music'):
            if i[-4::] == '.wav':
                self.playlist_list.append(i)
                self.playlist.addItem(i)
                self.playlist_list.sort()
                self.playlist.setSortingEnabled(True)
                self.playlist.sortItems()
        self.playlist.itemDoubleClicked.connect(self.play_pause)
        self.playlist.setCurrentRow(0)
        self.old_pos = self.pos()

        self.artist_lbl = QLabel('artist', self)
        self.artist_lbl.move(50, 352)
        self.artist_lbl.setStyleSheet(
            """
            *{
            color: '#999';
            font-size: 12px;
            }
            """)
        self.song_title_lbl = QLabel('song', self)
        self.song_title_lbl.move(50, 332)

        self.volume_slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(40)
        self.volume_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
            height: 12px;
            margin: 2px 0;
            }

            QSlider::handle:horizontal {
            background: white;
            margin: -2px 0;
            border-radius: 7px;
            }

            QSlider::add-page:horizontal {
            background: #555;
            margin: 2px 0;
            }

            QSlider::sub-page:horizontal {
            background: white;
            margin: 2px 0;
            }
            """)
        self.volume_slider.valueChanged.connect(self.volume)
        self.volume_slider.move(675, 335)

        self.current_volume = ''

        self.icon_mute = qta.icon('mdi.volume-variant-off', color='#999', scale_factor=1.5)
        self.icon_volume_high = qta.icon('mdi.volume-high', color='white', scale_factor=1.5)
        self.icon_volume_medium = qta.icon('mdi.volume-medium', color='white', scale_factor=1.5)
        self.btn_volume = QPushButton('', self)
        self.btn_volume.clicked.connect(self.mute_unmute)
        self.btn_volume.setIcon(self.icon_volume_medium)
        self.btn_volume.setStyleSheet('background: #111;')
        self.btn_volume.move(620, 322)

        mixer.init()
        mixer_music.set_volume(0.4)

        # self.duration = QSlider(QtCore.Qt.Horizontal, self)
        # self.duration.setRange(0, 0)
        # self.duration.sliderMoved.connect(self.change_pos)
        # self.duration.move(50, 50)

        self.path = ''
        self.old_path = ''

        self.position = int()

        self.show()

    def play_pause(self):
        if mixer_music.get_busy() == 0:
            self.path = 'music/' + self.playlist_list[self.playlist.currentRow()]
            if self.path == self.old_path:
                mixer_music.unpause()
                self.btn_play_pause.setIcon(QIcon('images/pause-fill.png'))
            elif self.path != self.old_path:
                self.position = self.playlist.currentRow()
                mixer_music.load(self.path)
                mixer_music.play()
                tag = self.artist_song(self.path)
                # self.duration.setRange(0, int(tag.duration))
                self.btn_play_pause.setIcon(QIcon('images/pause-fill.png'))

        elif mixer_music.get_busy() == 1:
            new_path = 'music/' + self.playlist_list[self.playlist.currentRow()]
            if self.path == new_path:
                mixer_music.pause()
                self.btn_play_pause.setIcon(QIcon('images/play-fill.png'))

            elif self.path != new_path:
                self.path = 'music/' + self.playlist_list[self.playlist.currentRow()]
                self.position = self.playlist.currentRow()
                mixer_music.load(self.path)
                mixer_music.play()
                tag = self.artist_song(self.path)
                # self.duration.setRange(0, int(tag.duration))
                self.btn_play_pause.setIcon(QIcon('images/pause-fill.png'))
                print(self.playlist.currentRow())

        self.old_path = 'music/' + self.playlist_list[self.playlist.currentRow()]

    def rewind(self):
        if mixer_music.get_pos() > 4000:
            mixer.stop()
            mixer_music.play()
        elif mixer_music.get_pos() < 4000:
            if self.position == 0:
                path = 'music/' + self.playlist_list[-1]
                self.position = len(self.playlist_list) - 1
                mixer_music.load(path)
                mixer_music.play()
                tag = self.artist_song(path)
                # self.duration.setRange(0, int(tag.duration))
            else:
                self.position -= 1
                path = 'music/' + self.playlist_list[self.position]
                mixer_music.load(path)
                mixer_music.play()
                tag = self.artist_song(path)
                # self.duration.setRange(0, int(tag.duration))

    def skip(self):
        if self.position == (len(self.playlist_list) - 1):
            self.position = 0
            path = 'music/' + self.playlist_list[self.position]
            mixer_music.load(path)
            mixer_music.play()
            tag = self.artist_song(path)
            # self.duration.setRange(0, int(tag.duration))
        else:
            self.position += 1
            path = 'music/' + self.playlist_list[self.position]
            mixer_music.load(path)
            mixer_music.play()
            tag = self.artist_song(path)
            # self.duration.setRange(0, int(tag.duration))

    def volume(self):
        mixer_music.set_volume(self.volume_slider.value()/100)
        self.current_volume = mixer_music.get_volume()
        if mixer_music.get_volume() == 0:
            self.btn_volume.setIcon(self.icon_mute)
        elif 0 < mixer_music.get_volume() < 0.5:
            self.btn_volume.setIcon(self.icon_volume_medium)
        elif mixer_music.get_volume() >= 0.5:
            self.btn_volume.setIcon(self.icon_volume_high)

    def mute_unmute(self):
        if mixer_music.get_volume() != 0:
            mixer_music.set_volume(0)
            self.volume_slider.setValue(0)
            self.btn_volume.setIcon(self.icon_mute)
        else:
            mixer_music.set_volume(0.4)
            self.volume_slider.setValue(40)
            self.btn_volume.setIcon(self.icon_volume_medium)

    def artist_song(self, x):
        tag = TinyTag.get(x)
        self.artist_lbl.setText(tag.artist)
        self.artist_lbl.adjustSize()
        self.song_title_lbl.setText(tag.title)
        self.song_title_lbl.adjustSize()
        return tag

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        moved = QtCore.QPoint(event.globalPos() - self.old_pos)
        self.move(self.x() + moved.x(), self.y() + moved.y())
        self.old_pos = event.globalPos()


app = QApplication(sys.argv)
root = MusicApp()

app.exec()
