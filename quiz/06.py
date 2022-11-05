from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import os
import sys

import json
import socket
import uuid
from ecdsa import SigningKey, VerifyingKey
import hashlib
import base64


def get_block_hash(block):
    data = dict()
    data['type'] = block['transaction']['type']
    data['data'] = sorted(block['transaction']['data'].copy().items())
    data['author'] = block['author']
    data['previous_hash'] = block['previous_hash']
    data = sorted(data.items())
    return hashlib.sha256(str(data).encode()).hexdigest()


def get_block_signature(block, key):
    data = dict()
    data['type'] = block['transaction']['type']
    data['data'] = sorted(block['transaction']['data'].copy().items())
    data['author'] = block['author']
    data['previous_hash'] = block['previous_hash']
    data = sorted(data.items())
    signature = key.sign(str(data).encode())
    return base64.b64encode(signature).decode()


def verify_block_hash(block):
    block_hash = get_block_hash(block)
    if block_hash != block['hash']:
        return False
    return True


def verify_block_signature(block):
    key = VerifyingKey.from_pem(block['author'].encode())
    data = dict()
    data['type'] = block['transaction']['type']
    data['data'] = sorted(block['transaction']['data'].copy().items())
    data['author'] = block['author']
    data['previous_hash'] = block['previous_hash']
    data = sorted(data.items())
    try:
        key.verify(base64.b64decode(block['signature'].encode()), str(data).encode())
    except:
        return False
    return True


def verity_block_chain(chain):
    if (not verify_block_hash(chain[0])) or chain[0]['transaction']['type'] != 'genesis':
        return False
    for i in range(1, len(chain)):
        if not verify_block_hash(chain[i]):
            return False
        if not verify_block_signature(chain[i]):
            return False
        if chain[i]['previous_hash'] != chain[i - 1]['hash']:
            return False
    return True


class Tab1(QWidget):
    def __init__(self, devs):
        super().__init__()

        self.devs = devs
        self.current_vote_id = -1

        self.wallet_group_box = QGroupBox('지갑')
        self.wallet_info_label = QLabel()
        self.wallet_info_label.setText('')
        self.wallet_generate_button = QPushButton('지갑 생성')
        self.wallet_generate_button.clicked.connect(self.generate_wallet)
        self.wallet_select_button = QPushButton('지각 선택')
        self.wallet_select_button.clicked.connect(self.select_wallet)
        self.wallet_layout = QHBoxLayout()
        self.wallet_layout.addWidget(self.wallet_info_label)
        self.wallet_layout.addWidget(self.wallet_generate_button)
        self.wallet_layout.addWidget(self.wallet_select_button)
        self.wallet_group_box.setLayout(self.wallet_layout)

        self.vote_list_group_box = QGroupBox('투표 목록')
        self.vote_list = dict()
        self.vote_list_widget = QListWidget()
        self.vote_list_widget.clicked.connect(self.select_vote)
        self.vote_list_layout = QVBoxLayout()
        self.vote_list_layout.addWidget(self.vote_list_widget)
        self.vote_list_group_box.setLayout(self.vote_list_layout)

        self.vote_group_box = QGroupBox('투표')
        self.question_label = QLabel()
        self.option1_button = QPushButton()
        self.option2_button = QPushButton()
        self.option3_button = QPushButton()
        self.option1_button.clicked.connect(self.vote1)
        self.option2_button.clicked.connect(self.vote2)
        self.option3_button.clicked.connect(self.vote3)
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
        self.main_layout.addWidget(self.wallet_group_box, 0, 0, 1, 2)
        self.main_layout.addWidget(self.vote_list_group_box, 1, 0, 1, 1)
        self.main_layout.addWidget(self.vote_group_box, 1, 1, 1, 1)
        self.main_layout.addWidget(self.vote_result_group_box, 2, 0, 1, 2)

        self.setLayout(self.main_layout)

        self.update_wallet_info()
        self.update_vote_list()



