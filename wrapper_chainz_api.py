

# build the url to fetch transaction data using chainz api
def build_url_tx(coin,transaction_hash):
    # documentation for chainz blockchain api usage: https://chainz.cryptoid.info/api.dws
    return f"https://chainz.cryptoid.info/{coin}/api.dws?q=txinfo&t="+ transaction_hash

# build the url to fetch wallet address data using chainz api    
def build_url_wl(coin,wallet_address):
    # documentation for chainz blockchain api usage: https://chainz.cryptoid.info/api.dws
    return f"https://chainz.cryptoid.info/{coin}/api.dws?q=addressinfo&a="+ wallet_address