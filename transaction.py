from collections import namedtuple

def TransactionDecoder(transaction):
    return namedtuple('Transaction', transaction.keys())(*transaction.values())

class Transaction:
    def __init__(self,transaction_dict):
        # convert all key/values pair into properties of the class
        for key in transaction_dict:
            setattr(self, key, transaction_dict[key])