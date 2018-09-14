import json

from blockchain import Blockchain

from flask import Flask, jsonify
from uuid import uuid4

app = Flask(__name__)  # initialize Flask app

node_identifier = str(uuid4()).replace('-', '')  # 현재 노드에 대한 전역 uuid를 생성한다

blockchain = Blockchain()  # Instantiate the Blockchain


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new Block"


@app.route('/transaction/new', methods=['POST'])
def new_transactions():
    return "We'll add a new transaction"


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain':blockchain.chain,
        'length':len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)