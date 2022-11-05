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

    def generate_wallet(self):
        self.devs.private_key = SigningKey.generate()
        self.devs.public_key = self.devs.private_key.get_verifying_key()
        self.devs.wallet_address = hashlib.sha256(self.devs.public_key.to_string()).hexdigest()
        if not os.path.exists('../wallets'):
            os.mkdir('../wallets')
        f = open(f'../wallets/{self.devs.wallet_address}.pem', 'wb')
        f.write(self.devs.private_key.to_pem())
        f.close()
        self.update_wallet_info()

    def select_wallet(self):
        path, _ = QFileDialog.getOpenFileName(self, '지갑 선택', '../wallets', 'PEM Files (*.pem)')
        if path == '':
            return
        f = open(path, 'rb')
        pem = f.read()
        f.close()
        self.devs.private_key = SigningKey.from_pem(pem)
        self.devs.public_key = self.devs.private_key.get_verifying_key()
        self.devs.wallet_address = hashlib.sha256(self.devs.public_key.to_string()).hexdigest()
        self.update_wallet_info()

    def update_wallet_info(self):
        self.wallet_info_label.setText(f'지갑 주소: {self.devs.wallet_address}')

    def update_vote_list(self):
        self.vote_list.clear()
        self.vote_list_widget.clear()
        for block in self.devs.chain:
            if block['transaction']['type'] == 'open':
                id = block['transaction']['data']['id']
                self.vote_list_widget.addItem(id)
                self.vote_list[id] = block['transaction']['data'].copy()
                self.vote_list[id]['total_vote'] = 0
                self.vote_list[id]['vote_count'] = dict()
                for option in block['transaction']['data']['options']:
                    self.vote_list[id]['vote_count'][option] = 0
            elif block['transaction']['type'] == 'vote':
                id = block['transaction']['data']['id']
                self.vote_list[id]['total_vote'] += 1
                self.vote_list[id]['vote_count'][block['transaction']['data']['vote']] += 1
        self.update_vote()

    def select_vote(self):
        self.current_vote_id = self.vote_list_widget.currentItem().text()
        self.update_vote()

    def update_vote(self):
        if self.current_vote_id not in self.vote_list:
            return

        self.question_label.setText(self.vote_list[self.current_vote_id]['question'])

        option1 = self.vote_list[self.current_vote_id]['options'][0]
        self.option1_button.setText(option1)
        self.option1_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        self.option1_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option1])

        option2 = self.vote_list[self.current_vote_id]['options'][1]
        self.option2_button.setText(option2)
        self.option2_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        self.option2_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option2])

        option3 = self.vote_list[self.current_vote_id]['options'][2]
        self.option3_button.setText(option3)
        self.option3_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        self.option3_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option3])

    def vote1(self):
        block = {
            'transaction': {
                'type': 'vote',
                'data': {
                    'id': self.current_vote_id,
                    'vote': self.option1_button.text()
                }
            },
            'author': self.devs.public_key.to_pem().decode(),
            'previous_hash': self.devs.chain[-1]['hash']
        }
        block['hash'] = get_block_hash(block)
        block['signature'] = get_block_signature(block, self.devs.private_key)
        self.devs.chain.append(block)
        for node in self.devs.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()

    def vote2(self):
        block = {
            'transaction': {
                'type': 'vote',
                'data': {
                    'id': self.current_vote_id,
                    'vote': self.option2_button.text()
                }
            },
            'author': self.devs.public_key.to_pem().decode(),
            'previous_hash': self.devs.chain[-1]['hash']
        }
        block['hash'] = get_block_hash(block)
        block['signature'] = get_block_signature(block, self.devs.private_key)
        self.devs.chain.append(block)
        for node in self.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()

    def vote3(self):
        block = {
            'transaction': {
                'type': 'vote',
                'data': {
                    'id': self.current_vote_id,
                    'vote': self.option3_button.text()
                }
            },
            'author': self.devs.public_key.to_pem().decode(),
            'previous_hash': self.devs.chain[-1]['hash']
        }
        block['hash'] = get_block_hash(block)
        block['signature'] = get_block_signature(block, self.devs.private_key)
        self.devs.chain.append(block)
        for node in self.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()




















