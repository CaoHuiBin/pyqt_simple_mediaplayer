from PyQt5 import QtMultimediaWidgets, QtMultimedia, QtWidgets, QtCore, QtGui
import sys


class MediaPlayer(QtWidgets.QWidget):
    def __init__(self):
        super(MediaPlayer, self).__init__()
        self.setWindowTitle("IMedia Player")
        self.setWindowIcon(QtGui.QIcon(r'E:\pyworkspace\media_player\images\logo.jpg'))

        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setFixedHeight(4)
        self.slider.setStyleSheet('''
             QSlider::add-page:Horizontal
             {
                background-color: rgb(87, 97, 106);
                height:4px;
             }
             QSlider::sub-page:Horizontal
            {
                background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(231,80,229, 255), stop:1 rgba(7,208,255, 255));
                height:4px;
             }
            QSlider::groove:Horizontal
            {
                background:transparent;
                height:4px;
            }''')

        self.media_screen = QtMultimediaWidgets.QVideoWidget()

        v_box = QtWidgets.QVBoxLayout()
        # 设置layout的间隔和与内的widget的边距
        v_box.setSpacing(0)
        v_box.setContentsMargins(0, 0, 0, 0)

        v_box.addWidget(self.media_screen)
        v_box.addWidget(self.slider)

        self.setLayout(v_box)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '确认退出', '你确定退出吗？',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def setSliderPostion(self, value):
        self.slider.setValue(value)


class Player(QtMultimedia.QMediaPlayer):
    def __init__(self, parent=None):
        super(Player, self).__init__()
        self.setObjectName('player')
        self.parent = parent
        self.playWidgets = self.parent
        # 关联视频进度和进度条位置
        self.positionChanged.connect(self.parent.setSliderPostion)
        self.metaDataAvailableChanged.connect(self.metaDataPrint)
        # self.
        self.mediaStatusChanged.connect(self.mediaChangedSlot)
        self.error.connect(self.handleError)
        file = QtCore.QFile('E:\\pyworkspace\\media_player\\test1.mp4')
        flag = file.open(QtCore.QIODevice.ReadOnly)
        print("flag:", flag)
        if not flag:
            print("Could not open file")
        path = file.fileName()
        print(path)
        url = QtCore.QUrl.fromLocalFile(path)

        content = QtMultimedia.QMediaContent(url)
        print(content.canonicalUrl())
        # 输出位置必须在setMedia前面
        self.setVideoOutput(self.parent.media_screen)
        self.setMedia(content)
        print('时长：', self.duration())

    def setPosition(self, p_int):
        print(p_int)

    def custom_postion(self, int):
        print('当前位置：', int)

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
        print('mediaStatus--------------', status)
        if status == 7:
            self.play()


app = QtWidgets.QApplication(sys.argv)

wid = MediaPlayer()
player = Player(wid)
player.play()

sys.exit(app.exec_())
