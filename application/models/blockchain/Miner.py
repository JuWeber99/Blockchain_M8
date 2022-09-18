import random

from application.models.blockchain import local_hashing
from application.models.blockchain.Block import Block
from application.models.blockchain.Blockchain import get_blockchain
from application.models.blockchain.CONFIG import mining_target
from application.models.blockchain.Mempool import get_mempool
from application.models.blockchain.Transaction import Transaction, Coinbase


class Miner:
    def __init__(self, own_public_key):
        self.public_key = own_public_key

    def check_agains_target(self, hash_string):
        hex = local_hashing.string_to_hex(hash_string)
        for i in range(1, mining_target + 1):
            if not hex[i] == "0":
                return False
        return True

# mine a block
    def mine(self):
        topmost_block = get_blockchain().get_topmost_block()
        assert isinstance(topmost_block, Block)
        hash_prev = topmost_block.get_hash()
        txs = get_mempool().tx
        for i in txs:
            assert isinstance(i, Transaction) or isinstance(i, Coinbase)
            if not i.is_valid():
                txs.remove(i)
        coinbase = Coinbase(self.public_key)
        txs.insert(0, coinbase)
        block = Block(hash_prev, txs, random.randint(0, 9999999999999999999999999999))
        hash = block.get_hash()
        # removed the while true wrapper just return true or false since the block only gets inserted if successful
        check = self.check_agains_target(hash)
        if check:
            success = get_blockchain().insert_block(block)
            if success:
                # we inserted a block and deleted the txns from mempool -> return success
                return True
            # invalid block mined try again -> return false
        return False
