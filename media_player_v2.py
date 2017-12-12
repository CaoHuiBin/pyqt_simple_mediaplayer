from PyQt5 import QtMultimediaWidgets, QtMultimedia, QtWidgets, QtCore, QtGui
import sys


class MediaPlayer(QtWidgets.QWidget):
    # 自定义信号
    _slider_draged = QtCore.pyqtSignal(int)

    def __init__(self):
        super(MediaPlayer, self).__init__()
        self.setWindowTitle("IMedia Player")
        self.setWindowIcon(QtGui.QIcon(r'E:\PyProject\pyqt_simple_mediaplayer\images\logo.jpg'))

        self.layout = QtWidgets.QVBoxLayout()
        self.slider = Slider(self)
        self.media_screen = QtMultimediaWidgets.QVideoWidget()
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

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '确认退出', '你确定退出吗？',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            if self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
                self.player.play()
            elif self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
                self.player.pause()
        elif e.key() == QtCore.Qt.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
                self.slider.show()
        elif e.key() == QtCore.Qt.Key_Enter:
            print("aa")
            if self.isFullScreen():
                self.showFullScreen()
            else:
                self.showFullScreen()

    def mouseDoubleClickEvent(self, e):
        if self.isFullScreen():
            self.showNormal()
            self.slider.show()
        else:
            self.showFullScreen()
            self.slider.hide()

    def mouseReleaseEvent(self, e):
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
        elif self.player.state() == QtMultimedia.QMediaPlayer.PausedState:
            self.player.play()

    def mouseMoveEvent(self, e):
        print(QtWidgets.QDesktopWidget.x())
        print(e.y())
        if e.y() > QtWidgets.QDesktopWidget.x() * 0.9:
            print('aaaa')


class Player(QtMultimedia.QMediaPlayer):
    def __init__(self, parent=None):
        super(Player, self).__init__()
        self.setObjectName('player')
        self.parent = parent
        self.playWidgets = self.parent.media_screen

        file = QtCore.QFile('E:\\PyProject\\media_player\\test.mp4')
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
                                (screen.size().height() - (size.height() + self.parent.slider.height())) / 2,
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
            self.play()


class Slider(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super(Slider, self).__init__(QtCore.Qt.Horizontal, parent)
        self.parent = parent
        self.setFixedHeight(8)
        # 设置开启鼠标点击事件
        self.setSliderDown(True)
        self.sliderReleased.connect(self.handle_slider_released)
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
        self.setValue(value)

    def handle_slider_pressed(self):
        pass

    def handle_slider_released(self):
        # 拖动滑块发射重新定位媒体播放位置信号
        self.parent._slider_draged.emit(self.value())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wid = MediaPlayer()
    wid.player.play()
    sys.exit(app.exec_())
