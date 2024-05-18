This app creates random mnemonics (12 word that helps to access crypto wallet) and checks in order to find valid wallets.

The chance of finding valid wallets are incredibly low (1/~2000^12).
These codes are not entirely mine i have just modified them and merge 3 main blockchains.

Failed attempts are listed on empty.txt. In order to be able to use bscscan and etherscan you need to sign up them and get API keys (put API keys into APIKeys.txy separated with comma and with order first eth theb bsc).

Thread counts can be optimized by your machine. Blockchain.com prevents to many requests (3 thread is optimal). Etherscan and Bscscan api's have limit to 5 requests per second.

reference: https://github.com/kubi34/Phase-key-Recovery-Tool
reference: https://github.com/MinightDev/BTC-Wallet-Recover