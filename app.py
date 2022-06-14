
# documentation for chainz blockchain api usage: https://chainz.cryptoid.info/api.dws
# as for now 13.06.2022, this blockchain explorer is only able to fetch data on transactions
# and wallet addres, the chainz api does not provide yet full information about a block
# only retrieving height, hash and block time 
from time import sleep
# Markup to render html element in template

from flask import Flask, render_template, request, Markup, redirect
import json
from fetch_data import fetch_and_format_cryptos_data



# start a server with this module as entry point
app = Flask(__name__)
#app.secret_key = "abc"
url_action = ""


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
