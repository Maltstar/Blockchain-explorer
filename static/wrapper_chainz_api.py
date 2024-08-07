import re

# build the url to fetch transaction data using chainz api
def build_url_tx(coin,transaction_hash):
    # documentation for chainz blockchain api usage: https://chainz.cryptoid.info/api.dws
    return f"https://chainz.cryptoid.info/{coin}/api.dws?q=txinfo&t="+ transaction_hash

# build the url to fetch wallet address data using chainz api    
def build_url_wl(coin,wallet_address):
    # documentation for chainz blockchain api usage: https://chainz.cryptoid.info/api.dws
    return f"https://chainz.cryptoid.info/{coin}/api.dws?q=addressinfo&a="+ wallet_address


crypto_symbols_alt = {
"Bitcoin":"btc",
"Ion":"ion",
"Litecoin":"ltc",
"DeFiChain":"dfi",
"Dash":"dash",
"DigiByte":"dgb",
"Syscoin":"sys",
"Divicoin":"divi",
"Strax":"strax",
"PutinCoin2":"put",
"Groestlcoin":"grs",
"Namecoin":"nmc",
"Peony":"pny",
"Firo":"firo",
"PandaCoin":"pnd",
"InfiniteCoin":"ifc",
"Vertcoin":"vtc",
"PeerCoin":"ppc",
"Bitcoin2":"btc2",
"Lynx":"lynx",
"PIVX":"pivx",
"Validity":"val",
"EarthCoin":"eac",
"NavCoin":"nav",
"Diamond":"dmd",
"UFO":"ufo",
"Unobtanium":"uno",
"Wagerr":"wgr",
"Ozziecoin":"ozc",
"Litecoin Cash": "lcc",
"Particl":"part",
"Gulden":"efl",
"cloak":"cloak",
"ECC":"ecc",
"Blocknet":"block",
"SafeDeal Coin":"sfd",
"ChessCoin 0.32%": "chess",
"42 coin":"42",
"Worldcoin":"wdc",
"DeepOnion":"onion",
"Einsteinium":"emc2",
"Dimecoin":"dime",
"Feathercoin":"ftc",
"Primecoin":"xpm",
"ZeitCoin":"zeit",
"BitCore":"btx",
"iXcoin":"ixc",
"NewYorkCoin":"nyc",
"BlackCoin":"blk",
"Alias":"alias",
"Manna":"manna",
"HTMLCOIN":"html",
"Auroracoin":"aur",
"Smileycoin":"smly",
"Titanoin":"ttn",
"Mooncoin":"moon",
"Quark":"qrk",
"GoldCoin":"glc",
"ColossusXT":"colx",
"CureCoin":"cure",
"Myriad":"xmy",
"BitcoinTrust":"bct",
"Granite":"grn",
"Terracoin":"trc",
"Denarius":"d",
"Okcash":"ok",
"Pinkcoin":"pink",
"I0Coin":"i0c",
"MonetaryUnit":"mue",
"freed":"freed",
"GlobalBoost":"bsty",
"Scolcoin":"scol",
"LiteDoge":"ldoge",
"Element":"hyp",
"Quantis":"quan",
"Artbyte":"aby",
"Phore":"phr",
"Experience points":"xp",
"ZENZO":"znz",
"Riecoin":"ric",
"Kobocoin":"kobo",
"Deutsche Mark":"dem",
"PakCoin":"pak",
"PWRB":"pwrb",
"Swing":"swing",
"Beanash":"bean",
"iCoin":"icn",
"Elite":"1337",
"NETKO":"netko",
"IO Coin":"ioc",
"SexCoin":"sxc",
"MotaCoin":"mota",
"TROLL":"troll",
"Noir":"nor",
"Bullion":"cbx",
"BitcoinPlus":"xbc",
"Biblepay":"bbp",
"Lanacoin":"lana",
"Slimcoin":"slm",
"GapCoin":"gap",
"Zetacoin":"zet",
"VeriCoin":"vrc",
"Trezarcoin":"tzc",
"Innova":"inn",
"PeepCoin":"pcn",
"DigitalCoin":"dgc",
"Konjungate":"konj",
"BitBlocks":"bbk",
"Megacoin":"mec",
"Beenode":"bnode",
"AudioCoin":"adc",
"ARCO":"arco",
"IFLT":"iflt",
"Noblecoin":"nobl",
"GlobalToken":"glt",
"KnoxFS":"kfx",
"Photon":"pho",
"JouleCoin":"xjo",
"super":"super",
"Civitas":"civ",
"Emerald":"emd",
"Bitmark":"marks",
"Icolcoin":"icol",
"EnergyCoin":"enrg",
"ZillionCoin":"zln",
"Audax":"audax",
"BolivarCoin":"boli",
"TheHolyRogerCoin":"roger",
"Sparks":"spk",
"Ignition":"ic",
"ImageCoin":"img",
"Influx":"infx",
"Guncoin":"gun",
"uTipcoin":"utip",
"CryptCoin":"crypt",
"Digitalmoneybits":"dmb",
"TajCoin":"taj",
"BitCloud":"btdx",
"CHBToken":"chbt",
"Veles":"vls",
"ImgCash":"imgc",
"BlockChainCoinX":"bccx",
"Mincoin":"mnc",
"Sprouts":"sprts",
"JoinCoin":"j",
"Scribe":"scribe",
"Goldcash":"gold",
"Bitradio":"bro",
"2Give":"2give",
"Argoneum":"agm",
"Argentum":"arg",
"AXIV":"axiv",
"B3Coin":"b3",
"BitBay":"bay",
"BlakeBitcoin":"bbtc",
"BitConnectoin":"bcc",
"Blakecoin":"blc",
"BitSend":"bsd",
"BITWIN24":"bwi",
"Bytecent":"byc",
"BYTZ":"bytz",
"'CACHE'Project": "cache",
"Canada-eCoin": "cdn",
"Circcash":"circ",
"Cirrus":"cirrus",
"Cirrus network":"cirrus-test",
"Coino":"cno",
"Certurium":"crt",
"CROWN":"crw",
"DopeCoin":"dope",
"Droidz":"drz",
"DevCoin":"dvc",
"egc":"egc",
"Electron":"elt",
"EmergencyCoin":"eny",
"Fortress":"fort",
"Groestlcoins":"grs-test",
"InfiniLooP":"il8p",
"Kore":"kore",
"Linx":"linx",
"Lithium":"lit",
"LKRcoin":"lkr",
"Meritcoins":"mrc",
"Myame Coin":"myg",
"Protocol":"ocp",
"bitFlowers":"petal",
"Piggycoin":"piggy",
"PotCoin":"pot",
"PeerCoin":"ppc-test",
"SkeinCurrency":"skc",
"Sterlingcoin":"slg",
"SolarCoin":"slr",
"Stakecoin":"stk",
"Strax":"strax-test",
"UniversalMolecule":"umo",
"Coin":"usdi",
"Verium":"vrm",
"Zerozed":"x0z",
"XCurrency":"xc",
"Magi":"xmg",
"trust":"trust",
"xvp":"xvp",
"Yantum":"yan",
"Wexcoin":"wex"    
}

# see documentation at https://chainz.cryptoid.info/api.dws
url_chain_api_summay = "https://chainz.cryptoid.info/explorer/api.dws?q=summary"

class Crypto_Symbol:

    def __init__(self):
        #fetch crypto symbol
        # summary = requests.get(url_chain_api_summay)
        # collection json object from the reponse
        #data_summary = summary.json()
        #print(data_summary)
        # store sorted crypto symbols
        #self.crypto_symbols = dict(sorted(crypto_symbols_alt.items()))
        self.crypto_symbols = {}
        # store symbol filtered according to search pattern, init value all cryptos
        #self.crypto_symbols_filtered = dict(sorted(crypto_symbols_alt.items()))
        self.crypto_symbols_filtered = {}

    def set(self, symbols):
        #fetch crypto symbol
       # summary = requests.get(url_chain_api_summay)
        # collection json object from the reponse
        #data_summary = summary.json()
        #print(data_summary)
        # store sorted crypto symbols
        self.crypto_symbols = dict(sorted(symbols.items()))
        # store symbol filtered according to search pattern, init value all cryptos
        self.crypto_symbols_filtered = dict(sorted(symbols.items()))

   
    def filter(self,search):
        coins_list = {}
        #print("filter")
        if len(search) != 0:
            #print("filter len(search) != 0")
            for key,value in self.crypto_symbols.items():
                # keeping only pair which matches search either by key or value, case insensitive
                if re.search(search, key, re.IGNORECASE) or re.search(search, value, re.IGNORECASE):
                #if search in key or search in value:
                    #print("search, key,value",search,key,value)
                    coins_list[key] = value
                   # print("coins_list",coins_list)
                    #print("coins_list sorted",sorted(coins_list))
                # return an ordered dict with coins pair
            self.crypto_symbols_filtered = dict(sorted(coins_list.items()))
        else:
            self.crypto_symbols_filtered = dict(sorted(self.crypto_symbols.items()))


my_Crypto = Crypto_Symbol()



def filter_coins(search):
    my_Crypto.filter(search)
    #print("filter_coins")

