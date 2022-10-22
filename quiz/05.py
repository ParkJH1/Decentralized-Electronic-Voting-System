from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import json
import socket
import uuid
import hashlib


def get_block_hash(block):
    data = dict()
    data['type'] = block['transaction']['type']
    data['data'] = sorted(block['transaction']['data'].copy().items())
    data = sorted(data.items())
    return hashlib.sha256(str(data).encode()).hexdigest()


class Tab1(QWidget):
    def __init__(self, devs):
        self.devs = devs
        self.current_vote_id = -1

        self.vote_list_group_box =  QGroupBox('투표 목록')
        self.vote_list = dict()
        self.vote_list_widget = QListWidget()
        self.vote_list_widget.clicked.connect(self.select_vote)
        self.vote_list_layout = QVBoxLayout()
        self.vote_list_layout.addWidget(self.vote_list_widget)
        self.vote_list_group_box.setLayout(self.vote_list_layout)

        
