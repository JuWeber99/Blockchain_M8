import threading

from application import getFlaskContext
from application.blockchain.Wallet import Wallet
from application.blockchain.Miner import Miner

wallet = Wallet()


def runMiner(wallet):
    miner = Miner(own_public_key=wallet.public_key)
    while True:
        miner.mine()


def startFlaskServer():
    app, port, hostname = getFlaskContext()
    app.run(host=hostname, port=port, debug=True, use_reloader=False)


if __name__ == "__main__":
    threading.Thread(target=lambda: runMiner(wallet)).start()
    threading.Thread(target=lambda: startFlaskServer()).start()

