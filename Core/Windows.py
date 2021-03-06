from PyQt5.QtWidgets import QLineEdit,QWidget,QVBoxLayout,QLabel,QTextBrowser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont,QColor
from Core import Gelbooru
import threading

main_windows = None

class Main_windows(QWidget):
    def __init__(self):
        global main_windows
        main_windows =self
        super(Main_windows, self).__init__()
        self.setMinimumWidth(250)
        self.setMaximumWidth(400)
        self.setMinimumHeight(180)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("Easy Download For GelBooru")
        layout = QVBoxLayout()

        label = QLabel()
        label.setFont(QFont("Timers", 10))
        label.setText('<b>将链接拖到输入框,自动下载原图</b><br>Tag链接则下载该Tag的全部原图<br>缩略图链接则下载该图片原图')

        self.edit_widget = QLineEdit()
        self.edit_widget.setMinimumHeight(80)
        self.edit_widget.setFont(QFont("Timers", 12))
        self.edit_widget.setPlaceholderText("")
        self.edit_widget.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.edit_widget.textChanged.connect(self.textChanged)

        layout.addWidget(label)
        layout.addWidget(self.edit_widget)
        self.setLayout(layout)

    def textChanged(self,text):
        """处理添加事件"""
        self.edit_widget.setText('')
        if text is None or len(text)<=1:
            self.edit_widget.setText('')
            return
        threading.Thread(target=self.handle_add, args=(text,)).start()

    def handle_add(self,url: str):
            print("处理链接[%s]" % url)
            change_title("处理中...")
            Gelbooru.deal_with_url(url)

def change_title(text:str):
    if main_windows is None:
        raise Exception("Windows为空，未创建过窗口")
    main_windows.setWindowTitle(text)

