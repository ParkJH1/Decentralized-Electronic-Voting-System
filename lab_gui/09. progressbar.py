from PyQt5.QtWidgets import *
import sys


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('제목')

        self.progressbar = QProgressBar()
        self.progressbar.setRange(0, 100)

        self.value = 0
        self.progressbar.setValue(self.value)

        self.button = QPushButton('+1')
        self.button.clicked.connect(self.button_click)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.progressbar, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.button, 1, 0, 1, 1)

        self.setLayout(self.grid_layout)

    def button_click(self):
        self.value += 1
        self.progressbar.setValue(self.value)


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())
