import json

from blockchain import Blockchain

from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)  # initialize Flask app

node_identifier = str(uuid4()).replace('-', '')  # 현재 노드에 대한 전역 uuid를 생성한다

blockchain = Blockchain()  # Instantiate the Blockchain


@app.route('/mine', methods=['GET'])
def mine():
    # 다음 블록의 proof값을 얻어내기 위해서 POW 알고리즘을 수행한다.
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof=last_proof)

    # proof값을 찾으면(채굴에 성공하면) 보상을 준다.
    # sender의 주소를 0으로 한다.
    # (원래 거래는 송신자, 수신자가 있어야하는데, 채굴에 대한 보상으로 얻은 코인의
    # sender가 없다.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    # 이전 블록의 hash값을 얻어와, 새 블록과 연결한다.
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof=proof, previous_hash=previous_hash)


    response = {
        'message' : 'New Block Forged',
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash' : block['previous_hash']

    }
    return jsonify(response), 200


@app.route('/transaction/new', methods=['POST'])
def new_transactions():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message' : f'Transaction will be added to Block {index}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)