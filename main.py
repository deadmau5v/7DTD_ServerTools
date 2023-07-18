import re
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class Select_server(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)

        # 设置logo
        uic.loadUi("./UIs/select_server.ui", self)
        logo_pixmap = QPixmap("./images/logo.png")
        self.logo.setPixmap(logo_pixmap.scaled(self.logo.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation))
        self.logo.setAlignment(Qt.AlignCenter)

        # icon
        self.setWindowIcon(QIcon("./images/icon.png"))
        self.setWindowTitle("七日杀服务器助手-选择服务器")

        self.btn1.clicked.connect(self.new_server)

    def new_server(self):
        """新建服务器弹窗"""
        msg = QDialog()
        msg_layout = QVBoxLayout()
        msg.setFixedSize(600, 300)
        msg.setWindowTitle("新建服务器")
        msg.setWindowIcon(QIcon("./images/icon.png"))
        server_name = QLineEdit()
        server_name.setPlaceholderText("请输入服务器名称")
        server_name.setFixedSize(400, 50)
        server_name.setAlignment(Qt.AlignCenter)
        server_name_box = QHBoxLayout()
        server_name_box.addStretch()
        server_name_box.addWidget(server_name)
        server_name_box.addStretch()

        msg_layout.addStretch()
        msg_layout.addLayout(server_name_box)
        btn_box = QHBoxLayout()
        yes_btn = QPushButton("确定")
        no_btn = QPushButton("取消")

        # 提示词款
        word = QLabel()
        word.close()

        def press_yes():
            if server_name.text().strip() == "":
                word.setText("请输入服务器名")
                word.setStyleSheet("color:red")
                word.show()
            elif not re.match(r"^[^\\/:*?\"<>|]+$", server_name.text()):
                word.setText('请输入正确的服务器名 不能包含/ \\ : * " < > | ？')
                word.setStyleSheet("color:red")
                word.show()
            else:
                # Todo 创建成功
                msg.close()


        yes_btn.clicked.connect(press_yes)
        no_btn.clicked.connect(msg.close)

        btn_box.addStretch()
        btn_box.addWidget(yes_btn)
        btn_box.addStretch()
        btn_box.addWidget(no_btn)
        btn_box.addStretch()
        msg_layout.addStretch()
        msg_layout.addLayout(btn_box)
        msg_layout.addStretch()

        msg_layout.addWidget(word)
        msg.setLayout(msg_layout)
        msg.show()
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    select_server = Select_server()
    select_server.show()

    app.exec_()
