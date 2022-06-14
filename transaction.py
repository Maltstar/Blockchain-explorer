from collections import namedtuple

def TransactionDecoder(transaction):
    return namedtuple('Transaction', transaction.keys())(*transaction.values())

class Transaction:
    def __init__(self,transaction_dict):
        #print('Transaction', str(type(transaction_dict)))
        #in case the response fetched is empty do not parse it
        if str(type(transaction_dict)) != "<class 'NoneType'>":
            # convert all key/values pair into properties of the class
            for key in transaction_dict:
                setattr(self, key, transaction_dict[key])
