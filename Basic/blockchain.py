import hashlib
import json
from time import time
from uuid import uuid4

# 블록 체인이 저장될 리스트와 또 다른 거래들이 저장되는 클래스
class Blockchain(object):
    def __init__(self):
        self.chain = []  # 블록 체인 저장 리스트
        self.current_transactions = []  # 거래 장부

        # 이전 블록이 없는 최초의 블록인 genesis block을 생성하고, proof를 추가한다.
        self.new_block(previous_hash=1, proof=100)

    # 새로운 블록을 만들고 체인에 추가하는 함수
    def new_block(self, proof, previous_hash=None):
        """
        블록체인에 새로운 블록 만들기

        :param proof: <int> proof는 Proof of WOrk 알고리즘에 의해서 제공된다
        :param previous_hash: (Optional) <str> 이전 블록의 해쉬값
        :return: <dict> 새로운 블록
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        # 거래 내역 초기화
        self.current_transactions = []

        self.chain.append(block)

        return block

    # 새로운 거래를 만들고 장부에 추가하는 함수
    def new_transaction(self, sender, recipient, amount):
        """
        새로 마이닝 되는 블록에 추가될 transcation을 만든다

        :param sender: <str> Sender의 주소
        :param recipient: <str> Recipient의 주소
        :param amount: <int> 거래 크기
        :return: <int> 이 거래를 포함할 블록의 index
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1


    def proof_of_work(self, last_proof):
        """
        POW 알고리즘 설명:
        - 앞에서 0의 개수가 4개가 나오는 hash(pp')을 만족시키는 p'을 찾는다
        - p 는 이전 블록의 proof, p'는 새로운 블록의 proof

        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Proof 검증 방법 : hash(last_proof, proof) 값의 앞 4자리가 0인가?

        :param last_proof: <int> 이전 블록의 proof 값
        :param proof: <int> 현재 블록의 proof 값
        :return: <bool> 옳은 값이라면 true, 그렇지 않으면 false값 반환
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # 블록을 해쉬하는 함수
    @staticmethod
    def hash(block):
        """
        블록에 대해서 SAH-256 해쉬를 생성
        :param block: <dict> Block
        :return: <str>
        """

        block_string = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


    # 제일 마지막 블록을 반환하는 함수
    @property
    def last_block(self):
        return self.chain[-1]
