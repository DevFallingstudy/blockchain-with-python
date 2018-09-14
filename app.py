import json

from blockchain import Blockchain

from flask import Flask, jsonify, request
from uuid import uuid4

app = Flask(__name__)  # initialize Flask app

node_identifier = str(uuid4()).replace('-', '')  # 현재 노드에 대한 전역 uuid를 생성한다

blockchain = Blockchain()  # Instantiate the Blockchain


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"


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