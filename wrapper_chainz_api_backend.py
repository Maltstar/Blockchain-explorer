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
"42 coin":"42",
"Alias":"alias",
"Argoneum":"agm",
"Artbyte":"aby",
"Auroracoin":"aur",
"B3Coin":"b3",
"Bean-Cash":"bean",
"Beenode":"bnode",
"Biblepay":"bbp",
"BitBay":"bay",
"BitBlocks":"bbk",
"BitCloud":"btdx",
"Bitcoin":"btc",
"BitcoinPlus":"xbc",
"BitCore":"btx",
"Bitmark":"marks",
"BitSend":"bsd",
"BlackCoin":"blk",
"BlakeBitcoin":"bbtc",
"Blakecoin":"blc",
"Blocknet":"block",
"BolivarCoin":"boli",
"BYTZ":"bytz",
"Canada-eCoin": "cdn",
"Cannacoin":"ccn",
"Catcoin":"cat",
"ChessCoin 32": "chess",
"Cirrus":"cirrus",
"Cirrus network test":"cirrus-test",
"CloakCoin":"cloak",
"Coino":"cno",
"ColossusXT":"colx",
"Compound":"comp",
"CROWN":"crw",
"CureCoin":"cure",
"Dash":"dash",
"DeFiChain":"dfi",
"Deutsche eMark":"em",
"Diamond":"dmd",
"DigiByte":"dgb",
"DigitalCoin":"dgc",
"Digitalmoneybits":"dmb",
"Dimecoin":"dime",
"Divicoin":"divi",
"Dogmcoin":"dogm",
"Doichain":"doi",
"e-Gulden":"efl",
"EarthCoin":"eac",
"ECC":"ecc",
"Einsteinium":"emc2",
"Electron":"elt",
"Element":"hyp",
"Elite":"1337",
"ELONCOIN":"emc",
"Emerald":"emd",
"EnergyCoin":"enrg",
"EverGreenCoin":"egc",
"Experience points": "xp",
"Feathercoin":"ftc",
"Firo":"firo",
"Freedomcoin":"freed",
"Goldcash":"gold",
"GoldCoin":"glc",
"Groestlcoin":"grs",
"Groestlcoin TestNet":"grstest",
"Hemis":"hms",
"HTMLCOIN":"html",
"I/O Coin":"ioc",
"I0Coin":"i0c",
"ImageCoin":"img",
"InfiniLooP":"il8p",
"InfiniteCoin":"ifc",
"Innova":"inn",
"iXcoin":"ixc",
"KnoxFS":"kfx",
"Kobocoin":"kobo",
"Komodo":"kmd",
"Lanacoin":"lana",
"Litecoin":"ltc",
"Litecoin cash": "lcc",
"LiteDoge":"ldoge",
"Lithium":"lit",
"Lynx":"lynx",
"Magi":"xmg",
"Mincoin":"mnc",
"Mooncoin":"moon",
"MotaCoin":"mota",
"My Game coin":"yg",
"Myriad":"xmy",
"Namecoin":"nmc",
"NETKO":"netko",
"NewYorkCoin":"nyc",
"Novacoin":"nvc",
"OC Protocol":"ocp",
"Okcash":"ok",
"PAC Protocol":"pac",
"PakCoin":"pak",
"PandaCoin":"pnd",
"Particl":"part",
"PeepCoin":"pcn",
"PeerCoin":"ppc",
"PeerCoin TestNet":"ppctest",
"Photon":"pho",
"Pinkcoin":"pink",
"PIVX":"pivx",
"PotCoin":"pot",
"Primecoin":"xpm",
"Puppycoin":"pup",
"PutinCoin v2":"put",
"Quantis":"quan",
"Quark":"qrk",
"Riecoin":"ric",
"SaluS":"sls",
"SatoshiCoin":"sat",
"SexCoin":"sxc",
"SkeinCurrency":"skc",
"Slimcoin":"slm",
"Smileycoin":"smly",
"Sparks":"spk",
"Sprouts":"sprts",
"Stakecoin":"stk",
"Sterlingcoin":"slg",
"Strax":"strax",
"Strax TestNet":"straxtest",
"Stronghands":"shnd",
"Swing":"swing",
"Syscoin":"sys",
"TajCoin":"taj",
"tekcoin":"tek",
"Terracoin":"trc",
"TheHolyRogerCoin":"roger",
"Trezarcoin":"tzc",
"TROLL":"troll",
"trust":"trust",
"UFO":"ufo",
"UFOhub":"ufohub",
"Unitus":"uis",
"UniversalMolecule":"umo",
"Unobtanium":"uno",
"Validity":"val",
"VeriCoin":"vrc",
"Verium":"vrm",
"Versacoin":"vcn",
"Vertcoin":"vtc",
"Wagerr":"wgr",
"Wexcoin":"wex  ",
"Worldcoin":"wdc",
"Yantum":"yan",
"ZENZO":"znz",
"Zetacoin":"zet"  ,
}

# see documentation at https://chainz.cryptoid.info/api.dws
url_chain_api_summay = "https://chainz.cryptoid.info/explorer/api.dws?q=summary"

class Crypto_Symbol:

    def __init__(self):
        self.crypto_symbols = {}
        # store symbol filtered according to search pattern, init value all cryptos
        self.crypto_symbols_filtered = {}

    def set(self, symbols):
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
    print("filter_coins")

