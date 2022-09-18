import json

from flask import Blueprint, render_template
from wtforms import DecimalField

from .forms import SendForm
from .models.blockchain.Blockchain import get_blockchain
from .models.blockchain.Transaction import Coinbase
from .models.blockchain.UTXO import UTXO
from .models.blockchain.Wallet import get_main_wallet, get_user_wallet

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

# get the balance a public key has
def get_balance_for_public_key(public_key):
    balance = 0
    # iterate all utxos for the public key and sum their value
    for utxo in get_blockchain().get_utxos(public_key):
        assert isinstance(utxo, UTXO)
        if utxo.public_key == public_key:
            balance = balance + utxo.message
    return balance


@main_bp.route('/')
# @login_required
def index():
    """Main page, displays balance"""
    wallet = get_main_wallet()
    balance = get_balance_for_public_key(wallet.public_key)
    return render_template('index.html', balance=balance)


@main_bp.route('/send', methods=['GET', 'POST'])
def send():
    """Provides a form to create and send a transaction"""
    form = SendForm()
    wallet = get_main_wallet()
    # print(get_blockchain().get_utxos(wallet.public_key))
    if form.validate_on_submit():
        # send 1 to user wallet
        wallet.send_money(get_blockchain(), [get_user_wallet().public_key], [1])
    return render_template('send.html', form=form, address=wallet.address)


@main_bp.route('/transactions', methods=['GET', 'POST'])
def transactions():
    """Displays all transactions from the user"""
    wallet = get_main_wallet()
    blocks = get_blockchain().blocks
    received_coinbase_txns = []
    sent_txns = []
    # iterate all blocks and search for txns of the current wallet (main wallet)
    # and search for the coinbase txns the wallet received and the txns it made
    for block in blocks:
        for tx in block.transactions:
            if isinstance(tx, Coinbase):
                for pk in tx.receiver_public_keys:
                    if wallet.public_key == pk:
                        received_coinbase_txns.append(tx)
                continue
            elif tx.utxos[0].public_key is wallet.public_key:
                sent_txns.append(tx)
    txns = sent_txns

    return render_template('transactions.html', txns=txns, cbtxns=received_coinbase_txns)


@main_bp.route('/mnemonic')
# @login_required
def mnemonic():
    """Displays the private key """
    wallet = get_main_wallet()
    return render_template('mnemonic.html', passphrase=wallet.private_key)


@main_bp.route('/last_block')
# @login_required
def get_last_block():
    """Displays the recovery passphrase"""

    return json.dumps(get_blockchain().get_topmost_block().get_dict(), indent=4)
