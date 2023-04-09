import sys
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize, Qt, QDate, QTime, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QLineEdit, QGridLayout


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def label_creation(self, label_name, x_position, y_position):

        self.label_temp = QLabel()

        font = QFont('Arial', 10, QFont.Bold)
        self.label_temp.setFont(font)
        self.label_temp.setAlignment(QtCore.Qt.AlignLeft)
        self.label_temp.move(x_position, y_position)

        self.layout().addWidget(self.label_temp)
        self.label_temp.setText(f'<font color="white">{label_name}</font>')

    def setup_UI(self):
        self.setWindowTitle("Fitynka App")
        self.setWindowIcon(QtGui.QIcon('PNG/logo.png'))
        self.setStyleSheet("background-color: pink;")
        self.setGeometry(700, 400, 400, 400)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel('Username:'), 0, 0)
        self.layout.addWidget(QLineEdit(), 0, 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setup_UI()
    window.show()

    app.exec()