import hashlib
import json
from time import time
from Advanced.pow import POW

class Blockchain(object):
    def __init__(self):
        self.chain = []  # 블록 체인 저장 리스트
        self.current_transactions = []  # 거래 장부
        self.POW = POW(4)

        # 이전 블록이 없는 최초의 블록인 genesis block을 생성하고, proof를 추가한다.
        self.new_block(data='Genesis', previous_hash=None)

    # 새로운 블록을 만들고 체인에 추가하는 함수
    def new_block(self, data, previous_hash=None):
        block = {
            'timestamp': time(),
            'data': data,
            'previous_hash': previous_hash,
            'hash': '',
            'nonce': 0
        }
        pow = self.POW.new_pow(block=block)
        nonce, hash_value = self.POW.run_pow(pow)

        block['hash'] = hash_value
        block['nonce'] = nonce

        self.chain.append(block)

        return block

    # 블록을 해쉬하는 함수
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    # 제일 마지막 블록을 반환하는 함수
    @property
    def last_block(self):
        return self.chain[-1]
