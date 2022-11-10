import os
from algosdk import account, mnemonic
from dotenv import load_dotenv
load_dotenv()


def get_account_by_participant(option):
    options = ["PHRASE_CUSTOMER", "PHRASE_TRANSPORTER", "PHRASE_SUPPLIER", "PHRASE_ROOT"]
    if option not in options:
        return "Please using phrase name:{}".format(options)

    phrase = os.environ.get(option).replace(', ', ' ')
    private_key = mnemonic.to_private_key(phrase)
    wallet_address = account.address_from_private_key(private_key)
    return private_key, wallet_address


if __name__ == '__main__':
    sk, address = get_account_by_participant('PHRASE_ROOT')
    print(sk, address)
