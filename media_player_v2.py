from PyQt5 import QtMultimediaWidgets, QtMultimedia, QtWidgets, QtCore, QtGui
import sys, os


class MediaPlayer(QtWidgets.QWidget):
    # 自定义信号
    _slider_draged = QtCore.pyqtSignal(int)

    def __init__(self):
        super(MediaPlayer, self).__init__()
        self.setWindowTitle("IMedia Player")
        icon_path = os.getcwd() + '\images\logo.jpg'
        self.setWindowIcon(QtGui.QIcon(icon_path))
        self.layout = QtWidgets.QVBoxLayout()
        self.slider = Slider(self)
        self.media_screen = PlayScreen(self)

        self.player = Player(self)
        self.setWidgets()
        self.setSignal()

    def setWidgets(self):
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.media_screen)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

    def setSignal(self):
        # 关联视频进度和进度条位置
        self.player.positionChanged.connect(self.slider.set_slider_position)
        self.player.metaDataAvailableChanged.connect(self.player.metaDataPrint)
        # self.
        self.player.mediaStatusChanged.connect(self.player.mediaChangedSlot)
        self.player.error.connect(self.player.handleError)
        self._slider_draged.connect(self.player.set_media_position)

    """
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '确认退出', '你确定退出吗？',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    """

    def keyPressEvent(self, e):
        print('Pressed Key:', e.key())
        if e.key() == QtCore.Qt.Key_Space:
            if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
                self.player.play()
            elif self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
                self.player.pause()
        elif e.key() == QtCore.Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                self.slider.show()
        elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            if not self.isFullScreen():
                self.showFullScreen()
                self.slider.hide()
        elif e.key() == QtCore.Qt.Key_Left:
            self.slider.setValue(self.slider.value() + 1000)
            self.slider.handle_slider_released()
        elif e.key == QtCore.Qt.Key_Right:
            pass


class PlayScreen(QtMultimediaWidgets.QVideoWidget):
    def __init__(self, parent=None):
        super(PlayScreen, self).__init__()
        self.parent = parent

    def mouseDoubleClickEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            if self.parent.isFullScreen():
                self.parent.showNormal()
                self.parent.slider.show()
            else:
                self.parent.showFullScreen()
                self.parent.slider.hide()

    def mouseReleaseEvent(self, e):
        if e.button() == QtCore.Qt.LeftButton:
            if self.parent.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
                self.parent.player.pause()
            elif self.parent.player.state() == QtMultimedia.QMediaPlayer.PausedState:
                self.parent.player.play()


class Player(QtMultimedia.QMediaPlayer):
    def __init__(self, parent=None):
        super(Player, self).__init__()
        self.setObjectName('player')
        self.parent = parent
        self.playWidgets = self.parent.media_screen
        media_path = os.getcwd() + '\\test1.mp4'
        file = QtCore.QFile(media_path)
        flag = file.open(QtCore.QIODevice.ReadOnly)
        print("flag:", flag)
        if not flag:
            print("Could not open file")
        path = file.fileName()
        url = QtCore.QUrl.fromLocalFile(path)

        content = QtMultimedia.QMediaContent(url)
        # 输出位置必须在setMedia前面
        self.setVideoOutput(self.parent.media_screen)
        self.setMedia(content)
        print('时长：', self.duration())

    def set_media_position(self, p_int):
        """重新定位媒体播放位置的槽"""
        self.setPosition(p_int)

    def metaDataPrint(self):
        print('歌名：', self.metaData('Title'))
        print('作者：', self.metaData('Author'))
        print('Date：', self.metaData('Date'))
        print('SampleRate：', self.metaData('SampleRate'))
        print('ChannelCount：', self.metaData('ChannelCount'))
        print('AudioCodec：', self.metaData('AudioCodec'))
        print('TrackNumber：', self.metaData('TrackNumber'))
        print('AudioBitRate：', self.metaData('AudioBitRate'))
        print('size:', self.metaData('Size'))
        print('Resolution', self.metaData('Resolution'))
        print('duration', self.metaData('Duration'))

        size = self.metaData('Resolution')
        print('长：', size.height())
        print('宽：', size.width())

        screen = QtWidgets.QDesktopWidget()

        # self.parent.media_screen.move((screen.size().width() - size.width()) / 2, (screen.size().height() / 2 - size.height()) / 2)
        self.parent.setGeometry((screen.size().width() - size.width()) / 2,
                                (screen.size().height() / 2 - (size.height() + self.parent.slider.height())) / 2,
                                size.width(), size.height() + self.parent.slider.height())
        self.parent.media_screen.resize(size.width(), size.height())

        self.parent.slider.setMaximum(self.metaData('Duration'))

        self.parent.show()

    def handleError(self, error):
        print(error)

    def closeProgram(self):
        sys.exit()

    def mediaChangedSlot(self, status):
        if status == 7:
            # self.play()
            pass


class Slider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(Slider, self).__init__(QtCore.Qt.Horizontal, parent)
        self.parent = parent
        self.setMouseTracking(True)
        self.setFixedHeight(8)
        # 设置开启鼠标点击事件
        self.setSliderDown(True)
        self.sliderReleased.connect(self.handle_slider_released)
        # self.valueChanged.connect(self.valueChanged)
        self.setStyleSheet('''
                     QSlider::add-page:Horizontal
                     {
                        background-color: rgb(87, 97, 106);
                        height:8px;
                     }
                     QSlider::sub-page:Horizontal
                    {
                        background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(80,231,149, 255), stop:1 rgba(7,208,255, 255));
                        height:8px;
                     }
                    QSlider::groove:Horizontal
                    {
                        background:transparent;
                        height:8px;
                    }
                    QSlider::handle:Horizontal
                    {
                        height: 12px;
                        width:8px;
                        color: green;
                        margin: -8 0px;
                    }
                    ''')

    def set_slider_position(self, value=0):
        self.setSliderPosition(value)
        # self.setValue(value)

    def handle_slider_pressed(self):
        pass

    def handle_slider_released(self):
        # 拖动滑块发射重新定位媒体播放位置信号
        self.parent._slider_draged.emit(self.value())

    def mouseMoveEvent(self, e):
        pass

    def mouseReleaseEvent(self, event):
        self.parent.player.setPosition(round(self.maximum() / self.width() * event.x()))


if __name__ == '__main__':
    print('path:', os.getcwd())
    app = QtWidgets.QApplication(sys.argv)
    wid = MediaPlayer()
    wid.player.play()
    sys.exit(app.exec_())
