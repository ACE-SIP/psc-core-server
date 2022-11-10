import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.future import transaction

from app.blockchain.account import get_account_by_participant
from app.blockchain.client import get_algod_client


def generate_algorand_keypair():
    sk, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(sk))
    print("My passphrase: {}".format(mnemonic.from_private_key(sk)))
    return sk, address


def send_transaction(sign_key, server_address, message=None):
    # get Algod Client
    algo_client = get_algod_client()
    print("My address: {}".format(server_address))
    account_info = algo_client.account_info(server_address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')))

    # build transaction
    params = algo_client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    amount = 100000
    unsigned_txn = transaction.PaymentTxn(server_address, params, receiver, amount, None, note=message)
    # sign transaction
    signed_txn = unsigned_txn.sign(sign_key)

    # submit transaction
    tx_id = algo_client.send_transaction(signed_txn)
    print("Signed transaction with txID: {}".format(tx_id))

    # wait for confirmation 
    try:
        confirmed_txn = transaction.wait_for_confirmation(algo_client, tx_id, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(
        confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account balance: {} microAlgos".format(account_info.get('amount')))
    print("Amount transferred: {} microAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))

    account_info = algo_client.account_info(server_address)
    print("Final Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")
    return tx_id


if __name__ == '__main__':
    private_key, my_address = get_account_by_participant('PHRASE_ROOT')
    note_data = {"org": "pharma supply chain", "product": "drug1", "date": "2022-05-17",
                 "anomaly": [{"temperature": 38, "description": "higher than required: under 35"}]}

    note = json.dumps(note_data).encode()
    send_transaction(private_key, my_address, note)
