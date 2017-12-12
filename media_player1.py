from PyQt5 import QtWidgets, QtMultimedia, QtMultimediaWidgets, QtCore
import sys


class Player(QtMultimedia.QMediaPlayer):
    def __init__(self):
        super(Player, self).__init__()

    def error(self, QMediaPlayer_Error=None):
        print("ssss")


app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.setWindowTitle("IPlayer")
layout = QtWidgets.QVBoxLayout()
player = Player()
vm = QtMultimediaWidgets.QVideoWidget()
player.setVideoOutput(vm)

layout.addWidget(vm)
widget.setLayout(layout)

file = QtCore.QFile('E:\\PyProject\\test.mp4')
flag = file.open(QtCore.QIODevice.ReadOnly)
print(flag)
if not flag:
    print("Could not open file")
else:
    qUrl = QtCore.QUrl.fromLocalFile("E:\\PyProject\\test.mp4")
    print(qUrl.path())
    content = QtMultimedia.QMediaContent(qUrl)
    b = content.isNull()
    print("isNull:", b)
    print("url:", content.canonicalResource())
    a = content.playlist()
    print("playList:", a)
    player.setMedia(content)
    widget.setWindowTitle("iplayer")
    widget.setGeometry(300, 300, 400, 300)

    player.setVideoOutput(vm)

    player.play()
    widget.show()

sys.exit(app.exec_())
