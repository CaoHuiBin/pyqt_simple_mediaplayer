from PyQt5 import QtMultimediaWidgets, QtMultimedia, QtWidgets, QtCore, QtGui
import sys


class MediaPlayer(QtMultimediaWidgets.QVideoWidget):
    def __init__(self):
        super(MediaPlayer, self).__init__()
        self.setGeometry(400, 400, 400, 300)
        self.setWindowTitle("IMedia Player")
        self.setWindowIcon(QtGui.QIcon(r'E:\pyworkspace\media_player\images\logo.jpg'))
        self.show()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '确认退出', '你确定退出吗？',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self, size):
        screen = QtWidgets.QDesktopWidget()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class Player(QtMultimedia.QMediaPlayer):
    def __init__(self, parent=None):
        super(Player, self).__init__()
        self.setObjectName('player')
        self.parent = parent
        self.playWidgets = self.parent
        self.positionChanged.connect(self.custom_postion)
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
        self.setVideoOutput(self.parent)
        self.setMedia(content)

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

        size = self.metaData('Resolution')
        print('长：', size.height())
        print('宽：', size.width())
        self.parent.setGeometry(400, 400, size.width(), size.height())

        screen = QtWidgets.QDesktopWidget()

        self.parent.move((screen.size().width()-size.width())/2, (screen.size().height()/2-size.height())/2)

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
widget = QtWidgets.QDesktopWidget()
print('desktop size:', widget.size())
sys.exit(app.exec_())
