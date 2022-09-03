from PyQt5.QtWidgets import *
import sys


class Tab1(QWidget):
    def __init__(self):
        super().__init__()

        #####################################################
        self.menu_group_box = QGroupBox('메뉴')

        self.fetch_vote_button = QPushButton('투표 조회')

        self.menu_hbox_layout = QHBoxLayout()
        self.menu_hbox_layout.addWidget(self.fetch_vote_button)

        self.menu_group_box.setLayout(self.menu_hbox_layout)
        #####################################################

        #####################################################
        self.vote_list_group_box = QGroupBox('투표 목록')

        self.vote_list = QListWidget()
        self.vote_list.addItem('투표 1')
        self.vote_list.addItem('투표 2')

        self.vote_list_vbox_layout = QVBoxLayout()
        self.vote_list_vbox_layout.addWidget(self.vote_list)

        self.vote_list_group_box.setLayout(self.vote_list_vbox_layout)
        #####################################################

        #####################################################
        self.vote_info_group_box = QGroupBox('투표 정보')

        self.question_label = QLabel()
        self.question_label.setText('투표 질문')

        self.option1_button = QPushButton('선택지 1')
        self.option2_button = QPushButton('선택지 2')
        self.option3_button = QPushButton('선택지 3')

        self.vote_info_vbox_layout = QVBoxLayout()
        self.vote_info_vbox_layout.addWidget(self.question_label)
        self.vote_info_vbox_layout.addWidget(self.option1_button)
        self.vote_info_vbox_layout.addWidget(self.option2_button)
        self.vote_info_vbox_layout.addWidget(self.option3_button)

        self.vote_info_group_box.setLayout(self.vote_info_vbox_layout)
        #####################################################

        self.vote_layout = QGridLayout()
        self.vote_layout.addWidget(self.menu_group_box, 0, 0, 1, 2)
        self.vote_layout.addWidget(self.vote_list_group_box, 1, 0, 1, 1)
        self.vote_layout.addWidget(self.vote_info_group_box, 1, 1, 1, 1)

        self.setLayout(self.vote_layout)



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
