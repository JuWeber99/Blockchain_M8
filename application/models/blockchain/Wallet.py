import codecs
import json
import os
import random
import string

from application.models.blockchain import crypto, local_hashing
from application.models.blockchain.Mempool import get_mempool
from application.models.blockchain.Transaction import UnsignedTransaction, Transaction
from application.models.blockchain.UTXO import UTXO

the_wallet = None
the_wallet2 = None


def load_from_file(c=""):
    with open(f"./private_key{c}.json", "r") as input_file:
        data = json.loads(input_file.read())
        return data["private_key"], data["password"]


def generate_new_wallet(password=None):
    password = crypto.generate_password() if password is None else password
    private_key = crypto.generate_private_pem_string(password_string=password)
    new_wallet = Wallet(unlock_pwd=password, unlock_privkey=private_key)
    new_wallet.save_to_file()
    return new_wallet


def get_main_wallet():
    global the_wallet
    if the_wallet is None:
        private_key, password = load_from_file()
        the_wallet = Wallet(password, private_key)
    return the_wallet


def get_main_wallet():
    global the_wallet
    if the_wallet is None:
        private_key, password = load_from_file("2")
        the_wallet = Wallet(password, private_key)
    return the_wallet


def get_user_wallet():
    global the_wallet
    if the_wallet is None:
        private_key, password = load_from_file()
        the_wallet = Wallet(password, private_key)
    return the_wallet


class Wallet:
    def __init__(self, unlock_pwd, unlock_privkey):
        self.password = unlock_pwd
        self.private_key = unlock_privkey
        self.public_key = crypto.generate_public_pem_string(self.private_key, self.password)
        self.address =codecs.encode(self.public_key.encode('utf-8'), 'base64')
        self.txns = []
        self.received_coinbase_txns = []
        self.balance = 0

    def send_money(self, chain, receiver_pks, msgs):
        print("sending money")
        money_to_send = 0
        for m in msgs:
            money_to_send = money_to_send + m
        tx = self.create_transaction(self.get_utxos_for_money(chain, money_to_send), receiver_pks, msgs)
        get_mempool().insert_transaction(tx)

    def get_transactions(self):
        return self.txns

    def get_utxos_for_money(self, chain, money):
        utxos = chain.get_utxos(self.public_key)
        assert isinstance(utxos, list)
        valid_utxos = []
        cumulated_balance = 0
        for i in utxos:
            if cumulated_balance >= money:
                break
            assert isinstance(i, UTXO)
            if chain.is_valid_UTXO(i):
                valid_utxos.append(i)
                cumulated_balance = cumulated_balance + i.message
        return valid_utxos

    def create_transaction(self, utxos, receiver_pks, msgs):
        unsigned = UnsignedTransaction(utxos=utxos, receiver_public_keys=receiver_pks, messages=msgs)
        tx = Transaction(utxos=utxos, receiver_public_keys=receiver_pks, messages=msgs,
                         signature=unsigned.sign(priv_key=self.private_key, password=self.password))
        return tx

    def insert_to_mempool(self, tx):
        get_mempool().insert_transaction(tx)

    def save_to_file(self):
        data = {
            "private_key": self.private_key,
            "password": self.password,
            "address": self.address
        }
        with open(f"./private_key_${self.address}.json", "w+") as output:
            output.write(json.dumps(data))
