from flask import Markup


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