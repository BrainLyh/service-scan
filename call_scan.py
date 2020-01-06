import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal

from sample_scan_1 import Ui_Form
from FtpModule import Ftp
from MySQLModule import MySQL


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ftp_scan.clicked.connect(lambda: self.ftp())
        self.mysql_scan.clicked.connect(lambda: self.mysql())
        self.update_text()

    def ftp(self):
        ftp = Ftp()
        ftp.threadpool()

    def mysql(self):
        mysql = MySQL()
        mysql.threadpool()

    def update_text(self):
        
        with open("./result.txt") as f:
            line = f.readlines()
            self.textBrowser.append(line[-1])

if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MainWindow()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
