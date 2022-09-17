from PyQt5.QtWidgets import *
import sys
import requests
import json


class Tab1(QWidget):
    def __init__(self):
        super().__init__()

        self.menu_group_box = QGroupBox('메뉴')
        self.fetch_vote_button = QPushButton('투표 조회')
        self.fetch_vote_button.clicked.connect(self.fetch_vote)
        self.menu_layout = QHBoxLayout()
        self.menu_layout.addWidget(self.fetch_vote_button)
        self.menu_group_box.setLayout(self.menu_layout)

        self.vote_list_group_box = QGroupBox()
        self.vote_list = dict()
        self.vote_list_widget = QListWidget()
        self.vote_list_layout = QVBoxLayout()
        self.vote_list_layout.addWidget(self.vote_list_widget)
        self.vote_list_group_box.setLayout(self.vote_list_layout)

        self.vote_group_box = QGroupBox()
        self.question_label = QLabel()
        self.option1_button = QPushButton('')
        self.option2_button = QPushButton('')
        self.option3_button = QPushButton('')
        self.vote_layout = QVBoxLayout()
        self.vote_layout.addWidget(self.question_label)
        self.vote_layout.addWidget(self.option1_button)
        self.vote_layout.addWidget(self.option2_button)
        self.vote_layout.addWidget(self.option3_button)
        self.vote_group_box.setLayout(self.vote_layout)

        self.vote_result_group_box = QGroupBox()
        self.option1_progressbar = QProgressBar()
        self.option2_progressbar = QProgressBar()
        self.option3_progressbar = QProgressBar()
        self.vote_result_layout = QVBoxLayout()
        self.vote_result_layout.addWidget(self.option1_progressbar)
        self.vote_result_layout.addWidget(self.option2_progressbar)
        self.vote_result_layout.addWidget(self.option3_progressbar)
        self.vote_result_group_box.setLayout(self.vote_result_layout)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.menu_group_box, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.vote_list_group_box, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.vote_group_box, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.vote_result_group_box, 2, 0, 1, 2)

        self.setLayout(self.grid_layout)

    def fetch_vote(self):
        res = requests.get('http://127.0.0.1:5000/list')
        block_chain = json.loads(res.text)
        self.vote_list.clear()
        self.vote_list_widget.clear()
        for block in block_chain:
            if block['type'] == 'open':
                self.vote_list_widget.addItem(block['data']['id'])
            elif block['type'] == 'vote':
                pass


class Tab2(QWidget):
    def __init__(self):
        super().__init__()

        self.form_layout = QFormLayout()

        self.question_line_edit = QLineEdit()

        self.option1_line_edit = QLineEdit()
        self.option2_line_edit = QLineEdit()
        self.option3_line_edit = QLineEdit()

        self.publish_clear_layout = QHBoxLayout()

        self.publish_button = QPushButton('게시')
        self.publish_button.clicked.connect(self.publish_form)
        self.clear_button = QPushButton('초기화')
        self.clear_button.clicked.connect(self.clear_form)

        self.publish_clear_layout.addWidget(self.publish_button)
        self.publish_clear_layout.addWidget(self.clear_button)

        self.form_layout.addRow('질문:', self.question_line_edit)
        self.form_layout.addRow('선택지:', self.option1_line_edit)
        self.form_layout.addRow('', self.option2_line_edit)
        self.form_layout.addRow('', self.option3_line_edit)
        self.form_layout.addRow('', self.publish_clear_layout)

        self.setLayout(self.form_layout)

    def publish_form(self):
        headers = {'Content-Type': 'application/json'}

        question = self.question_line_edit.text()
        option1 = self.option1_line_edit.text()
        option2 = self.option2_line_edit.text()
        option3 = self.option3_line_edit.text()

        data = {
            'question': question,
            'options': [option1, option2, option3]
        }

        res = requests.post(
            'http://127.0.0.1:5000/open',
            data=json.dumps(data),
            headers=headers
        )
        print(res.text)
        self.clear_form()

    def clear_form(self):
        self.question_line_edit.setText('')
        self.option1_line_edit.setText('')
        self.option2_line_edit.setText('')
        self.option3_line_edit.setText('')


class CentralizedElectronicVotingSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('중앙 블록체인 투표 시스템')

        self.tab1 = Tab1()
        self.tab2 = Tab2()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab1, '투표')
        self.tabs.addTab(self.tab2, '투표 생성')

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabs)

        self.setLayout(self.vbox)


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    cevs = CentralizedElectronicVotingSystem()
    cevs.show()
    sys.exit(app.exec())