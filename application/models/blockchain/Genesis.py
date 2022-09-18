from application.models.blockchain.Transaction import Coinbase
from application.models.blockchain.Wallet import get_main_wallet

# we dont need this key we just take the one from the wallet
def genesis_coinbase():
    return Coinbase(get_main_wallet().public_key)
