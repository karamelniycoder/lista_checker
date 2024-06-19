from eth_account.messages import encode_defunct
from web3 import Web3


class Wallet:
    def __init__(self, privatekey: str):
        self.privatekey = privatekey
        self.account = Web3().eth.account.from_key(privatekey)
        self.address = self.account.address


    def sign_message(self, text: str):
        message = encode_defunct(text=text)
        signed_message = self.account.sign_message(message)
        return signed_message.signature.hex()
