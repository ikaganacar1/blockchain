# import threading
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from typing import Optional

import requests
import json
from termcolor import colored
import logging
import threading





BSCAPI = ''


with open('random wallet checker/APIKeys.txt','r') as f:
    for line in f:
       _ , BSCAPI = line.split(":")
            
     
def subforce():
    count = 0
    while True:    
        MNEMONIC: str = generate_mnemonic(language="english", strength=256)
        PASSPHRASE: Optional[str] = None  # "meherett"
        bip44_hdwallet: BIP44HDWallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        bip44_hdwallet.from_mnemonic(
            mnemonic=MNEMONIC, language="english", passphrase=PASSPHRASE
        )
        bip44_hdwallet.clean_derivation()
        bip44_derivation: BIP44Derivation = BIP44Derivation(
            cryptocurrency=EthereumMainnet, account=0, change=False, address=0)
        bip44_hdwallet.from_path(path=bip44_derivation)

        me = bip44_hdwallet.mnemonic()
        addr = bip44_hdwallet.address()


        #BSC
        try:
            bsc =requests.get(f'https://api.bscscan.com/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={BSCAPI}', timeout=5000.0)
        except requests.exceptions.RequestException as err:
            print(colored("Requests Error" , color="red"))
            logging.warning(err)    
        
        bscJson =bsc.json()
        dumpBSCJson = json.dumps(bscJson)

        loadBSCJson = json.loads(dumpBSCJson)
        bscTransaction = loadBSCJson["status"]
        #os.system("cls")
        #print(colored("BSC" , color="white"))
        
        if int(bscTransaction) >0:
            print(colored(f"Has transaction history {me} {addr}", color="green"))
            with open("valid.txt", "a") as bscWallets:
                    bscWallets.write("\nWallet: " + me + " BSC CHAIN " + addr)
            break
        else:
            count +=1
            #print(colored(f"{bscTransaction} {me} {addr}", color="yellow"))
            with open("random wallet checker/empty.txt", "a") as ethWallets:
                    ethWallets.write("\nWallet:"+str(count)+" " + me + " BSC CHAIN " + addr)
                    
            print(colored(f"{addr} - BSC",color="yellow"))


        bip44_hdwallet.clean_derivation()

def mainforce():

    for i in range(5):
        p = threading.Thread(target=subforce)
        p.start()

            
if __name__ == '__main__' :
    mainforce() 