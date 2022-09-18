import threading

from application import getFlaskContext, views
from application.models.blockchain.Blockchain import get_blockchain
from application.models.blockchain.Wallet import Wallet, get_main_wallet, get_user_wallet
from application.models.blockchain.Miner import Miner

# run the miner singletons mine function in a loop
def runMiner(wallet):
    miner = Miner(own_public_key=wallet.public_key)
    while True:
        miner.mine()


# setup function for flask server
def startFlaskServer():
    app, port, hostname = getFlaskContext()
    app.config["SECRET_KEY"] = "put any long random string here"
    app.register_blueprint(views.main_bp)
    app.run(host=hostname, port=port, debug=True, use_reloader=False)

# run miner in background thread to keep mining while also running flask server in another thread
if __name__ == "__main__":
    threading.Thread(target=lambda: runMiner(get_main_wallet())).start()
    threading.Thread(target=lambda: startFlaskServer()).start()
    ##get_main_wallet().send_money(get_blockchain(), [get_user_wallet().public_key], [40])
    # startFlaskServer()
