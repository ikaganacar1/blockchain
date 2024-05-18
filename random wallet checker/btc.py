import mnemonic
import bip32utils
import requests
import logging
import time
import threading
from termcolor import colored

def generate_mnemonic():
    mnemo = mnemonic.Mnemonic("english")
    return mnemo.generate(strength=128)

def recover_wallet_from_mnemonic(mnemonic_phrase):
    seed = mnemonic.Mnemonic.to_seed(mnemonic_phrase)
    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    child_key = root_key.ChildKey(44 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    address = child_key.Address()
    balance = check_BTC_balance(address)
    return mnemonic_phrase, balance, address


def check_BTC_balance(address, retries=3, delay=5):
    for attempt in range(retries):
        try:
            
            response = requests.get(f"https://blockchain.info/balance?active={address}", timeout=10,headers={'User-agent':'your bot 0.1'})
            response.raise_for_status()
            data = response.json()
            balance = data[address]["final_balance"]
            return balance / 100000000
        except requests.RequestException as e:
            if attempt < retries - 1:
                logging.error(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
    return 0

def mainloop():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    mnemonic_count = 0
    while True:
        mnemonic_phrase = generate_mnemonic()
        mnemonic_phrase, balance, address = recover_wallet_from_mnemonic(mnemonic_phrase)
        #logging.info(f"Mnemonic Phrase: {mnemonic_phrase}")
        print(colored(f"{address} - BTC",color="yellow"))
        if balance > 0:
            logging.info(f"Found wallet with non-zero balance: {balance} BTC")
            with open("wallet.txt", "a") as f:
                f.write(f"Mnemonic Phrase: {mnemonic_phrase}\n")
                f.write(f"Wallet Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n\n")
        else:
            with open("random wallet checker/empty.txt", "a") as ethWallets:
                    ethWallets.write("\nWallet:"+str(mnemonic_count)+" " + mnemonic_phrase + " BTC CHAIN " + address)
                    
            #logging.info(f"Wallet with zero balance {balance}. Trying again...")
        mnemonic_count += 1
        #logging.info(f"Total Mnemonic Phrases generated: {mnemonic_count}\n")
        
def mainforce():
    _1 = threading.Thread(target=mainloop)
    _1.start()

    _2 = threading.Thread(target=mainloop)
    _2.start()

    _3 = threading.Thread(target=mainloop)
    _3.start()

if __name__ == "__main__":
    mainforce()
    