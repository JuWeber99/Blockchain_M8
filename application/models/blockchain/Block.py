import json

from application.models.blockchain import local_hashing


class Block:
    def __init__(self, hash_previous_block, transactions, nonce):
        self.transactions = transactions
        self.hash_previous_block = hash_previous_block
        self.nonce = nonce

    def get_hash(self):
        data = self.get_dict()
        json_data = json.dumps(data)
        return local_hashing.hash(json_data)

    def get_dict(self):
        transaction_hash_list = []
        for i in self.transactions:
            transaction_hash_list.append(i.get_hash())
        return {
            "transaction_hashes": transaction_hash_list,
            "hash_previous_block": self.hash_previous_block,
            "nonce": self.nonce
        }
