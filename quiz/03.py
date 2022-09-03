from PyQt5.QtWidgets import *
import sys


class Tab1(QWidget):
    def __init__(self):
        super().__init__()


class Tab2(QWidget):
    def __init__(self):
        super().__init__()

        self.form_layout = QFormLayout()

        self.question_line_edit = QLineEdit()
        self.option1_line_edit = QLineEdit()
        self.option2_line_edit = QLineEdit()
        self.option3_line_edit = QLineEdit()

        self.publish_button = QPushButton('게시')
        self.clear_button = QPushButton('초기화')

        self.publish_clear_hbox_layout = QHBoxLayout()
        self.publish_clear_hbox_layout.addWidget(self.publish_button)
        self.publish_clear_hbox_layout.addWidget(self.clear_button)

        self.form_layout.addRow('질문: ', self.question_line_edit)
        self.form_layout.addRow('선택지: ', self.option1_line_edit)
        self.form_layout.addRow('', self.option2_line_edit)
        self.form_layout.addRow('', self.option3_line_edit)
        self.form_layout.addRow('', self.publish_clear_hbox_layout)

        self.setLayout(self.form_layout)


class CentralizedElectronicVotingSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('중앙 전자 투표 시스템')

        self.tab1 = Tab1()
        self.tab2 = Tab2()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab1, '투표')
        self.tabs.addTab(self.tab2, '투표 생성')

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.tabs)

        self.setLayout(self.vbox_layout)


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    cevs = CentralizedElectronicVotingSystem()
    cevs.show()
    sys.exit(app.exec())
