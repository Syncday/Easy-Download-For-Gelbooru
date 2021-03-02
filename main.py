from PyQt5.QtWidgets import QApplication
from Core import Windows


if __name__ == '__main__':
    app = QApplication([])
    windows = Windows.Windows()
    windows.show()
    app.exec_()

