from flask import Flask

from application.models.blockchain.Wallet import generate_new_wallet, Wallet

app = Flask(__name__)
port = 9999
hostname = "127.0.0.1"


def getFlaskContext():
    return app, port, hostname
