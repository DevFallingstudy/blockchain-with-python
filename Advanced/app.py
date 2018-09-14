from Advanced.blockchain import Blockchain

if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.new_block('hello', previous_hash=blockchain.last_block['hash'])
    blockchain.new_block('my name is YS', previous_hash=blockchain.last_block['hash'])

    for item in blockchain.chain:
        print("---")
        print("data : " + item['data'])
        print("hash : " + item['hash'])
        print("previous hash : " + str(item['previous_hash']))