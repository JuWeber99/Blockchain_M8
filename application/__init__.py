from flask import Flask

app = Flask(__name__)
port = 9999
hostname = "127.0.0.1"


def getFlaskContext():
    return app, port, hostname
