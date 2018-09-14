from Advanced.blockchain import Blockchain
from Advanced.pow import POW

if __name__ == '__main__':
    pow = POW(4)
    blockchain = Blockchain()
    blockchain.new_block('hello', previous_hash=blockchain.last_block['hash'])
    blockchain.new_block('my name is YS', previous_hash=blockchain.last_block['hash'])


    for item in blockchain.chain:
        print("---")
        print("data : " + item['data'])
        print("hash : " + item['hash'])
        print("previous hash : " + str(item['previous_hash']))
        print()
        current_pow = pow.new_pow(item)
        pow.validate_pow(current_pow, item['nonce'])