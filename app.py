from blockchain import Blockchain

from flask import Flask
from uuid import uuid4

app = Flask(__name__)  # initialize Flask app

node_identifier = str(uuid4()).replace('-', '')  # 현재 노드에 대한 전역 uuid를 생성한다

blockchain = Blockchain() # Instantiate the Blockchain



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)