from wrapper_chainz_api_backend import build_url_tx, build_url_wl, my_Crypto
from format import format_results
import requests
from transaction import Transaction
from flask import Markup, Response, json
from time import sleep


#################################################
#   Fetch data wrapper api Functions
#################################################

def fetch_and_format_cryptos_data(coin,hash,operator):

    if operator == 't':
        # build url for api, transaction hash
        transaction_url = build_url_tx(coin,hash)
    elif operator == 'w':
            # build url for api, wallet address
        transaction_url = build_url_wl(coin,hash)

    # fetch crypto data and error message
    data_response = fetch_cryptos_data(transaction_url)
    my_crypto = data_response['crypto_data']
    no_matches = data_response['error']
    # converting crypto data class results to dict
    # to parse easyli result data
    my_crypto_dict = my_crypto.__dict__
    # formating response from api as html elements
    result = format_results(my_crypto_dict,coin,operator)
    result_response ={'result':result,'error':no_matches}
    return result_response

# fetch data from apis
def fetch_cryptos_data(transaction_url):
    no_matches = ''
    max_retries = 3
    # maximal 10 times crypto data fetchen
    for i in range(0,max_retries):
        

        # fetch crypto data from passed url
        transation_data = requests.get(transaction_url)
        

        # collection json object from the reponse
        print('transation_data',transation_data)
        dict_data = transation_data.json()

        # create a class from the json fetched data
        # in order to later on :
        # 1- extract the key/value pair per __dict__ without having to parse all pairs manually
        # 2- dynamically display the key/value pair as html elements
        # without having to code manually an html element per value key/pair 
        my_crypto = Transaction(dict_data)
        #my_crypto = {}
        #checking response
        if my_crypto.__dict__ != {}:
            break
            print('fetch_cryptos_data, response',my_crypto.__dict__)
        # otherwise wait 10s and fetch data again
        sleep(10)
    #check if data has been found otherwise indicating no matches
    if my_crypto.__dict__ == {}:
        no_matches = Markup("<br><br>Kein Ergebnisse gefunden :( <br> Versuchen Sie eine Hash auf dem aktuellen ausgewälten Blockchain Netzwerk und den richtigen Feld einzutragen.")
    # build a response with crypto data fetched and built-in error message
    response = {'crypto_data':my_crypto,'error':no_matches}    
    return response

def fetch_summary():
    # see documentation at https://chainz.cryptoid.info/api.dws 
    url_chain_api_summary = "https://chainz.cryptoid.info/explorer/api.dws?q=summary"
    # Make a request to the JSON Placeholder API
    summary = requests.get(url_chain_api_summary)
    data = summary.json() 
    return data

# fetch summary and return it as http response
def fetch_symbols():

    # # see documentation at https://chainz.cryptoid.info/api.dws 
    # url_chain_api_summary = "https://chainz.cryptoid.info/explorer/api.dws?q=summary"
    # # Make a request to the JSON Placeholder API
    # summary = requests.get(url_chain_api_summary)
    # data = summary.json()
    
    data = fetch_summary()
    # setup body of the response
    resp = Response(response=json.dumps(data),status=200)
    # setup header to allow CORS for anyon
    #print("resp.data",resp.data)
    #json_resp_data = resp.data.json()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    #print('response',resp)
   
    return resp

def update_coin_list():
    
    # Object is of form { "crypto name":symbol}
    crypto_symbols = {}
    symbols = fetch_summary()
    for symbol, value in symbols.items():
        crypto_symbols[symbol] = value["name"]
    my_Crypto.set(crypto_symbols)
    print('my_Crypto',my_Crypto.crypto_symbols)
    return my_Crypto