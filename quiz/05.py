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



