from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys

import json
import socket
import uuid


class Tab1(QWidget):
    def __init__(self, devs):
        super().__init__()
        self.devs = devs
        self.current_vote_id = -1

        self.vote_list_group_box = QGroupBox('투표 목록')
        self.vote_list = dict()
        self.vote_list_widget = QListWidget()
        self.vote_list_widget.clicked.connect(self.select_vote)
        self.vote_list_layout = QVBoxLayout()
        self.vote_list_layout.addWidget(self.vote_list_widget)
        self.vote_list_group_box.setLayout(self.vote_list_layout)

        self.vote_group_box = QGroupBox('투표')
        self.question_label = QLabel(self)
        self.option1_button = QPushButton()
        self.option2_button = QPushButton()
        self.option3_button = QPushButton()
        self.vote_layout = QVBoxLayout()
        self.vote_layout.addWidget(self.question_label)
        self.vote_layout.addWidget(self.option1_button)
        self.vote_layout.addWidget(self.option2_button)
        self.vote_layout.addWidget(self.option3_button)
        self.vote_group_box.setLayout(self.vote_layout)

        self.vote_result_group_box = QGroupBox('투표 결과')
        self.option1_progressbar = QProgressBar()
        self.option2_progressbar = QProgressBar()
        self.option3_progressbar = QProgressBar()
        self.vote_result_layout = QVBoxLayout()
        self.vote_result_layout.addWidget(self.option1_progressbar)
        self.vote_result_layout.addWidget(self.option2_progressbar)
        self.vote_result_layout.addWidget(self.option3_progressbar)
        self.vote_result_group_box.setLayout(self.vote_result_layout)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.vote_list_group_box, 0, 0, 1, 1)
        self.main_layout.addWidget(self.vote_group_box, 0, 1, 1, 1)
        self.main_layout.addWidget(self.vote_result_group_box, 1, 0, 1, 2)

        self.setLayout(self.main_layout)

        self.update_vote_list()

    def update_vote_list(self):
        self.vote_list.clear()
        self.vote_list_widget.clear()
        for block in self.devs.chain:
            if block['type'] == 'open':
                vote_id = block['data']['id']
                self.vote_list_widget.addItem(vote_id)
                self.vote_list[vote_id] = block['data']
                self.vote_list[vote_id]['total_vote'] = 0
                self.vote_list[vote_id]['vote_count'] = dict()
                for option in block['data']['options']:
                    self.vote_list[vote_id]['vote_count'][option] = 0
            elif block['type'] == 'vote':
                vote_id = block['data']['id']
                self.vote_list[vote_id]['total_vote'] += 1
                self.vote_list[vote_id]['vote_count'][block['data']['vote']] += 1
        self.update_vote()

    def select_vote(self):
        self.current_vote_id = self.vote_list_widget.currentItem().text()
        self.update_vote()

    def update_vote(self):
        if self.current_vote_id not in self.vote_list:
            return

        self.question_label.setText(self.vote_list[self.current_vote_id]['question'])

        self.option1_button.setText(self.vote_list[self.current_vote_id]['options'][0])
        self.option1_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        option1_text = self.vote_list[self.current_vote_id]['options'][0]
        self.option1_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option1_text])

        self.option2_button.setText(self.vote_list[self.current_vote_id]['question'])
        self.option2_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        option2_text = self.vote_list[self.current_vote_id]['options'][1]
        self.option2_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option2_text])

        self.option3_button.setText(self.vote_list[self.current_vote_id]['question'])
        self.option3_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        option3_text = self.vote_list[self.current_vote_id]['options'][2]
        self.option3_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option3_text])

    def vote1(self):
        block = {
            'type': 'vote',
            'data': {
                'id': self.current_vote_id,
                'vote': self.option1_button.text()
            }
        }
        self.devs.chain.append(block)
        for node in self.devs.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()

    def vote2(self):
        block = {
            'type': 'vote',
            'data': {
                'id': self.current_vote_id,
                'vote': self.option2_button.text()
            }
        }
        self.devs.chain.append(block)
        for node in self.devs.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()

    def vote3(self):
        block = {
            'type': 'vote',
            'data': {
                'id': self.current_vote_id,
                'vote': self.option3_button.text()
            }
        }
        self.devs.chain.append(block)
        for node in self.devs.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()


class Tab2(QWidget):
    def __init__(self, devs):
        super().__init__()
        self.devs = devs

        self.form_layout = QFormLayout()

        self.question_line_edit = QLineEdit()

        self.option1_line_edit = QLineEdit()
        self.option2_line_edit = QLineEdit()
        self.option3_line_edit = QLineEdit()

        self.publish_clear_layout = QHBoxLayout()
        self.publish_button = QPushButton('게시')
        self.publish_button.clicked.connect(self.publish_vote)
        self.clear_button = QPushButton('초기화')
        self.clear_button.clicked.connect(self.clear_vote)
        self.publish_clear_layout.addWidget(self.publish_button)
        self.publish_clear_layout.addWidget(self.clear_button)

        self.form_layout.addRow('질문:', self.question_line_edit)
        self.form_layout.addRow('선택지:', self.option1_line_edit)
        self.form_layout.addRow('', self.option2_line_edit)
        self.form_layout.addRow('', self.option3_line_edit)
        self.form_layout.addRow('', self.publish_clear_layout)

        self.setLayout(self.form_layout)


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    devs = Tab1(None)
    devs.show()
    sys.exit(app.exec_())
