import eth
import bsc
import btc

import threading

if __name__ == "__main__":

    bs = threading.Thread(target=bsc.mainforce)
    bs.start()

    et = threading.Thread(target=eth.mainforce)
    et.start()

    bt = threading.Thread(target=btc.mainforce)
    bt.start()

