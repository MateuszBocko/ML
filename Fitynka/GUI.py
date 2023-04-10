import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from cryptography.fernet import Fernet

def decrypt(token: bytes, key: bytes):
    return Fernet(key).decrypt(token)

class AdminWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_UI(self):
        self.setWindowTitle("Fitynka App - Admin Window")
        self.setWindowIcon(QtGui.QIcon('PNG/logo.png'))
        self.setStyleSheet("background-color: pink;")
        self.setGeometry(700, 400, 300, 150)

        # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

        # username
        layout.addWidget(QLabel('Username:'), 0, 0)
        layout.addWidget(QLineEdit(), 0, 1)

        # password
        layout.addWidget(QLabel('Password:'), 1, 0)
        layout.addWidget(QLineEdit(echoMode=QLineEdit.EchoMode.Password), 1, 1)

        # buttons
        self.login_button = QPushButton('Log in')
        layout.addWidget(self.login_button, 2, 0, 1, 0)
        self.login_button.clicked.connect(self.login_button_func)
        # show the window
        self.show()

    def login_button_func(self):
        f = open("CREDS/creds.txt", "rb")
        creds = f.read()

        key = Fernet.generate_key()
        print(type(creds))

        creds = decrypt(creds, key).decode()
        print(creds)


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_UI(self):
        self.setWindowTitle("Fitynka App")
        self.setWindowIcon(QtGui.QIcon('PNG/logo.png'))
        self.setStyleSheet("background-color: pink;border-color: transparent")
        self.setGeometry(700, 400, 300, 150)

        # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

        # new cursor
        CURSOR_NEW = QtGui.QCursor(QtGui.QPixmap('PNG/test.jpg'))
        #self.setCursor(CURSOR_NEW)

        style_for_buttons = (
            "border-radius: 15px; "
            "border :2px solid ;"
            "border-top-color : ghostwhite; "
            "border-left-color :ghostwhite;"
            "border-right-color :ghostwhite;"
            "border-bottom-color : ghostwhite"
        )

        # Admin button
        self.admin_button = QPushButton('Trener')
        self.admin_button.setFont(QFont('Boulder', 15))
        self.admin_button.setStyleSheet(style_for_buttons)
        layout.addWidget(self.admin_button)
        self.admin_button.clicked.connect(self.button_admin_click)

        self.trainee_button = QPushButton('Podopieczny')
        self.trainee_button.setFont(QFont('Times', 15))
        self.trainee_button.setStyleSheet(style_for_buttons)
        layout.addWidget(self.trainee_button)

        self.show()

    def button_admin_click(self):
        self.admin_window = AdminWindow()
        self.admin_window.setup_UI()
        self.admin_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setup_UI()
    sys.exit(app.exec())