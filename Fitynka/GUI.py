import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from encrypting import is_correct_password
from db_operations import DatabaseOperations
from config import logo
logo()

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_UI(self):
        self.setWindowTitle("Fitynka App")
        self.setWindowIcon(QtGui.QIcon('PNG/logo.png'))
        self.setStyleSheet("background-color: pink;border-color: transparent")
        self.setGeometry(700, 400, 350, 220)

        # set the grid layout
        layout = QGridLayout()
        self.setLayout(layout)

        # new cursor
        CURSOR_NEW = QtGui.QCursor(QtGui.QPixmap('PNG/cursor.png'))
        self.setCursor(CURSOR_NEW)

        style_for_buttons = (
            "border-radius: 15px; "
            "border :2px solid ;"
            "border-top-color : ghostwhite; "
            "border-left-color :ghostwhite;"
            "border-right-color :ghostwhite;"
            "border-bottom-color : ghostwhite"
        )

        # username
        self.username = QLabel('Login:')
        self.username.setFont(QFont('Boulder', 10))
        self.username.setStyleSheet("border :0px; font-weight: bold")
        layout.addWidget(self.username, 0, 0)

        self.username_input = QLineEdit()
        self.username_input.setFont(QFont('Boulder', 10))
        self.username_input.setStyleSheet(style_for_buttons)
        layout.addWidget(self.username_input, 0, 1)

        # password
        self.password = QLabel('Hasło:')
        self.password.setFont(QFont('Boulder', 10))
        self.password.setStyleSheet("border :0px; font-weight: bold")
        layout.addWidget(self.password, 1, 0)

        self.password_input = QLineEdit(echoMode=QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont('Boulder', 10))
        self.password_input.setStyleSheet(style_for_buttons)
        layout.addWidget(self.password_input, 1, 1)

        # Login button
        self.login_button = QPushButton("Zaloguj się")
        self.login_button.setFont(QFont('Boulder', 10))
        self.login_button.setStyleSheet(style_for_buttons)
        self.login_button.clicked.connect(self.login_to_account)
        layout.addWidget(self.login_button, 2, 1)


        # Rejestracja
        self.username = QLabel('<center>Nie posiadasz konta? Załóż je w prosty sposób!')
        self.username.setFont(QFont('Boulder', 10))
        self.username.setStyleSheet("border :0px ;")
        layout.addWidget(self.username, 4, 0, 1, 0, Qt.AlignBottom)

        self.login_button = QPushButton("Załóż konto")
        self.login_button.setFont(QFont('Boulder', 10))
        self.login_button.setStyleSheet(style_for_buttons)
        self.login_button.clicked.connect(self.login_to_account)
        layout.addWidget(self.login_button, 5, 0, 1, 0)

        self.show()

    def login_to_account(self):

        db_ops = DatabaseOperations()

        query = '''SELECT * FROM users WHERE login = %s'''
        try:
            result = db_ops.execute_queries(query, (self.username_input.text(),))
            password_result = is_correct_password(salt=eval(result[2]), pw_hash=eval(result[3]), password=self.password_input.text())
            if password_result == False:
                QMessageBox.about(self, "Błąd logowania", "<b><p align='center'>Hasło niepoprawne!<br>")
            else:
                QMessageBox.about(self, "Sukces", "<b><p align='center'>Logowanie pomyslne!<br>")
                #TODO check if user is admin/customer and open proper window with features for specific group
        except:
            QMessageBox.about(self, "Błąd logowania", "<b><p align='center'>Login niepoprawny!<br>")

    def remind_password(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setup_UI()
    sys.exit(app.exec())