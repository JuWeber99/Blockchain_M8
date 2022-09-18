import json

from application.models.blockchain import local_hashing


class UTXO:
    def __init__(self, tx_hash, public_key, message):
        self.tx_hash = tx_hash
        self.public_key = public_key
        self.message = message

    def get_dict(self):
        return {
            "tx_hash": self.tx_hash,
            "public_key": self.public_key,
            "message": self.message
        }

    def get_hash(self):
        return local_hashing.hash(json.dumps(self.get_dict()))
