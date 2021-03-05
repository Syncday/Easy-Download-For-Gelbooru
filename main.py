from PyQt5.QtWidgets import QApplication
from Core import Windows
from Core import Config


if __name__ == '__main__':
    app = QApplication([])
    windows = Windows.Main_windows()
    windows.show()
    app.exec_()

