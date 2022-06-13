
# documentation for chainz blockchain api usage: https://chainz.cryptoid.info/api.dws
# as for now 13.06.2022, this blockchain explorer is only able to fetch data on transactions
# and wallet addres, the chainz api does not provide yet full information about a block
# only retrieving height, hash and block time 
from time import sleep
# Markup to render html element in template

from flask import Flask, render_template, request, url_for, session, Markup, redirect
#from flask_session import Session
import requests
import json
from transaction import Transaction
from wrapper_chainz_api import build_url_tx, build_url_wl



# start a server with this module as entry point
app = Flask(__name__)
app.secret_key = "abc"
url_action = ""


#################################################
#   Format Response to HTML Elements Functions
#################################################

# return html element either with hyperlink or text from chainzapi response
def manage_hyperlink(key,coin,value):
    format_result = ""
    # create hyperlinks to parse transaction and wallet address 
    if key == "tx":
        url = build_url_local_transaction(coin,value)
        format_result += Markup("<br><strong>{0}</strong> <br> <a href={1}>{2}</a>".format(key,url,value))
        print('manage_hyperlink tx',format_result)
    elif key == "addr":
        url = build_url_local_wallet(coin,value)
        format_result += Markup("<br><strong>{0}</strong> <br> <a href={1}>{2}</a>".format(key,url,value))
        print('manage_hyperlink addr',format_result)
        # only display value    
    else:
        format_result += Markup("<br><strong>{0}</strong> <br> {1}".format(key,value))
        print('manage_hyperlink else',format_result)

    return format_result

# dynamically format the key/value pair of dict as html elements
# """ Example of Response:
# {'hash': '51e950fb5dae48e96b3e674205b312c05f154c4077ec22adbf15ad445ff1e833',
#  'block': 1687289,
#  'index': 0,
#  'timestamp': 1655137287,
#  'confirmations': 2,
#  'fees': -2.49347601,
#  'total_input': None,
#  'inputs': [], 
#  'total_output': 2.49347601,
#  'outputs': [
#      {'addr': 'XmzfivrzYQ7B7oBMZKwPRdhjB1iNvX71XZ',
#       'amount': 1.10460988,
#       'script': '76a9147c086eada12bdb10a265c16c08a7ae87366bd48188ac'},
#      {'addr': 'XoDo3w4ZUqn93uL3FeRNb9fgfXvgg7BvDC',
#       'amount': 1.27775684,
#       'script': '76a914897c151a6aa235b7880fb7d34dacaca178ca039588ac'},
#      {'addr': 'Xr421hEMiXCt67RC6K48jPR89mZMF5a7wD',
#       'amount': 0.11110929,
#       'script': '76a914a88b1eab808c8341fb2cbe2af192c76cab7a6d4b88ac'}
#       ]
# } """
def format_results(my_crypto_dict,coin,operator=""):

    result = ""
    
    # the input data are in form of a dictionary
    # value are either single element, a dictionary or a list of dictionary
    for key,value in my_crypto_dict.items():
            result += Markup("<br>")
            #print(result)
            #1 value the element is a list 
            if str(type(value)) == "<class 'list'>":
                result += Markup("<br> <strong>{0}:</strong> <br>".format(key))
                #print(result)
                # parsing each element of the list
                for element in value:
                    # format for each element of the list
                    result += Markup("<br>")
                    # so far result on the list have been only dictionnary but testing to be sure
                    if str(type(element)) == "<class 'dict'>":
                        for sub_key,sub_value in element.items():
                        # create an html element with all keys witin value
                            if str(type(sub_value)) == "<class 'dict'>":
                                result += Markup("<br> <strong >{0}:</strong>".format(sub_key))
                                for under_key,under_value in sub_value.items():
                                    result += manage_hyperlink(under_key,coin,under_value)
                            else:
                                result += manage_hyperlink(sub_key,coin,sub_value)
            #2- value is a dictionary 
            elif str(type(value)) == "<class 'dict'>":
                # parsing it
                for under_key,under_value in sub_value.items():
                    result += manage_hyperlink(under_key,coin,under_value)
            #3- value is a single element 
            else:
                result += Markup('<br> <strong>{0}:</strong> {1} <br>'.format(key,value))
                #print(result)

    return result

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


#################################################
#   Routing Functions
#################################################

# build the url to transaction page served
def build_url_local_transaction(coin,hash):
    url = f"/blockchain/{coin}/transaction/{hash}"
    return url

# build the url to wallet page served
def build_url_local_wallet(coin,hash):
    url = f"/blockchain/{coin}/wallet/{hash}"
    return url



# Routing für Home
@app.route("/")
def home():
    return render_template("index.html")

# manage input sent by user and redirect to the appropriate page accordingly
@app.route("/blockchain/redirect/<coin>", methods= ["GET", "POST"])
def redirect_route(coin):

    url_action = "/blockchain/" + coin
    # Check, ob POST-Daten vorliegen
    if request.method == "POST":

        # Transaction und wallet von Anfrage an Server abgreifen
        transaction_hash = str(request.form["transaction"]) # ["username"]: der gleiche Name wie die Eingabemaske vom HTML-Formular
        wallet_address = str(request.form["address"]) # ["username"]: der gleiche Name wie die Eingabemaske vom HTML-Formular

        if(transaction_hash!=""):
            # redirecting to transaction page
            url_action = "/blockchain/" + coin + "/transaction/" + transaction_hash

        elif(wallet_address!=""):
            # redirecting to wallet address page
            url_action = "/blockchain/" + coin + "/wallet/" + wallet_address
        else:
            url_action = "/blockchain/" + coin

        # excute redirection
    return redirect(url_action)


# home page of the selected coin with the search fields transaction, wallet
@app.route("/blockchain/<coin>", methods= ["GET", "POST"])
def blockchain(coin):

    print('HI, FUnction BLOCKCHAIN')
    # for compatibility with the api, the api takes only lower case crypto name
    coin = coin.lower() 

    global result
    result = ""
    global url_action
    # redirect to route manager when the user send the input data
    # Can not used directly the propertie action of the form htlm element 
    # otherwise the 1st call to render_template can not be set to any transaction
    # wallet address pages since no input data have been sent yet.
    # So "action" in the form is always setup with a previous link 
    # since the current link depends on
    # the inputs data when the formular has been filled and the data sent by a click of the button
    url_action = "/blockchain/redirect/" + coin

    print('url_action',url_action)
    # zeige das Formular an
    return render_template("index_coin.html",dataToRender=url_action,result=result,coin=coin.upper())

# transaction page matching the transaction searched by the user, display also the form to continu the search
# for test purpose use https://chainz.cryptoid.info/
@app.route("/blockchain/<coin>/transaction/<tx>", methods= ["GET", "POST"])
def transaction(coin,tx):

    #global result
    result = ""
    error_result = ""
    if request.method == "GET":
        response_data = fetch_and_format_cryptos_data(coin,tx,'t')
        result = response_data['result']
        error_result = response_data['error']


    # ansonsten zeige das Formular an
    return render_template("index_coin.html",dataToRender=url_action,result=result,coin=coin.upper(),no_matches=error_result)

# wallet page matching the wallet address searched by the user, display also the form to continu the search
# for test purpose use https://chainz.cryptoid.info/
@app.route("/blockchain/<coin>/wallet/<wallet_address>", methods= ["GET", "POST"])
def address(coin,wallet_address):

    global result
    result = ""
    if request.method == "GET":
        response_data = fetch_and_format_cryptos_data(coin,wallet_address,'w')
        result = response_data['result']
        error_result = response_data['error']
 
    # ansonsten zeige das Formular an
    return render_template("index_coin.html",dataToRender=url_action,result=result,coin=coin.upper(),no_matches=error_result)


# Server starten
app.run()
