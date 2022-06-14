from wrapper_chainz_api import build_url_tx, build_url_wl
from format import format_results
import requests
from transaction import Transaction
from flask import Markup
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
        dict_data = transation_data.json()

        # create a class from the json fetched data
        # in order to later on :
        # 1- extract the key/value pair per __dict__ without having to parse all pairs manually
        # 2- dynamically display the key/value pair as html elements
        # without having to code manually an html element per value key/pair 
        my_crypto = Transaction(dict_data)
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