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

