import hashlib
import json

class POW(object):
    def __init__(self, targetBits):
        self.targetBits = targetBits  # POW에 사용될 목표 비트

    def new_pow(self, block):
        pow = {
            'block': block,
            'target': None
        }

        target_str = 10**(64-self.targetBits)
        target = int("0x"+str(target_str), 16)
        pow['target'] = target

        return pow

    def prepare_data_for_calcuate(self, pow, nonce):
        data = {
            'previous_hash': pow['block']['previous_hash'],
            'data': pow['block']['data'],
            'timestamp': pow['block']['timestamp'],
            'target_bits': pow['target'],
            'nonce': nonce
        }

        data_bytes = json.dumps(data, sort_keys=True).encode()

        return data_bytes

    def run_pow(self, pow):
        hash_value = None
        nonce = 0
        maxNonce = 100000000000000000000

        print('mining the block containing '+pow['block']['data'])

        while nonce < maxNonce:
            data = self.prepare_data_for_calcuate(pow=pow, nonce=nonce)
            hash_value = hashlib.sha256(data).hexdigest()
            hash_int = int("0x"+hash_value, 16)
            target_int = pow['target']

            if hash_int < target_int:
                break
            else:
                nonce += 1

        print()

        return nonce, hash_value

    def validate_pow(self, pow, nonce):
        target_data = self.prepare_data_for_calcuate(pow=pow, nonce=nonce)
        target_hash = hashlib.sha256(target_data).hexdigest()

        print(target_hash)
        print(pow['block']['hash'])