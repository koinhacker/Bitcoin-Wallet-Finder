from lxml import html
import time
from colorama import Fore, Style
from hdwallet import HDWallet
from hdwallet.utils import generate_entropy
from hdwallet.symbols import BTC as SYMBOL
from typing import Optional
import json
import multiprocessing
from multiprocessing import Pool
import threading

import requests

koinhacker = '''

██╗░░██╗░█████╗░██╗███╗░░██╗██╗░░██╗░█████╗░░█████╗░██╗░░██╗███████╗██████╗░
██║░██╔╝██╔══██╗██║████╗░██║██║░░██║██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗
█████═╝░██║░░██║██║██╔██╗██║███████║███████║██║░░╚═╝█████═╝░█████╗░░██████╔╝
██╔═██╗░██║░░██║██║██║╚████║██╔══██║██╔══██║██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
██║░╚██╗╚█████╔╝██║██║░╚███║██║░░██║██║░░██║╚█████╔╝██║░╚██╗███████╗██║░░██║
╚═╝░░╚═╝░╚════╝░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
--------------------------------------------------------
[x] Software: Bitcoin Wallet Finder
[x] Author: KoinHacker
[x] Github: koinhacker
[x] Version: 1.0
--------------------------------------------------------
Donate me BTC: bc1qhzems2lsstx795ae8er698zp0vvcvg3p39e3yr
========================================================

▀▀█▀▀ ░█▀▀█ ▀█▀ ─█▀▀█ ░█─── 　 ░█──░█ ░█▀▀▀ ░█▀▀█ ░█▀▀▀█ ▀█▀ ░█▀▀▀█ ░█▄─░█ 
─░█── ░█▄▄▀ ░█─ ░█▄▄█ ░█─── 　 ─░█░█─ ░█▀▀▀ ░█▄▄▀ ─▀▀▀▄▄ ░█─ ░█──░█ ░█░█░█ 
─░█── ░█─░█ ▄█▄ ░█─░█ ░█▄▄█ 　 ──▀▄▀─ ░█▄▄▄ ░█─░█ ░█▄▄▄█ ▄█▄ ░█▄▄▄█ ░█──▀█
'''

PRINT = Fore.GREEN + koinhacker + Fore.RESET
print('\n\n', Fore.RED, str(PRINT), Style.RESET_ALL, '\n')

r = 1
cores = 8

def finder(r):     
    z = 1
    w = 0
    while True:
        # Choose strength 128, 160, 192, 224 or 256
        STRENGTH: int = 256  # Default is 128
        # Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese or korean
        LANGUAGE: str = "english"
        ENTROPY: str = generate_entropy(strength=STRENGTH)
        PASSPHRASE: Optional[str] = None

        hdwallet: HDWallet = HDWallet(symbol=SYMBOL, use_default_path=False)

        hdwallet.from_entropy(
            entropy=ENTROPY, language=LANGUAGE, passphrase=PASSPHRASE
        )

        hdwallet.from_index(44, hardened=True)
        hdwallet.from_index(0, hardened=True)
        hdwallet.from_index(0, hardened=True)
        hdwallet.from_index(0)
        hdwallet.from_index(0)
        
        addr: str = hdwallet.p2pkh_address()
        p2sh_address: str = hdwallet.p2sh_address()
        p2wpkh_address: str = hdwallet.p2wpkh_address()
        p2wpkh_in_p2sh_address: str = hdwallet.p2wpkh_in_p2sh_address()
        p2wsh_address: str = hdwallet.p2wsh_address()
        p2wsh_in_p2sh_address: str = hdwallet.p2wsh_in_p2sh_address()
        mnemonic: str = hdwallet.mnemonic()
        private_key: str = hdwallet.private_key()

        try: 
            urlblock = "https://bitcoin.atomicwallet.io/address/" + addr
            respone_block = requests.get(urlblock)
            byte_string = respone_block.content
            source_code = html.fromstring(byte_string)
            xpatch_txid = '/html/body/main/div/div[2]/div[1]/table/tbody/tr[3]/td[2]'
            treetxid = source_code.xpath(xpatch_txid)
            xVol = str(treetxid[0].text_content())
            balance_str = str(xVol)
            balance_value = int(balance_str.split()[0])
            balance = int(balance_str.split()[0])
            ifbtc = '0 BTC'
        except Exception as e:
            balance = 0
            print(e)
            time.sleep(3)
            pass


        print('Winner Wallet:',Fore.GREEN, str(w), Fore.YELLOW,'Total Scan:',Fore.WHITE, str(z), Fore.YELLOW, Fore.YELLOW, 'P2PKH:', Fore.WHITE, str(addr), Fore.YELLOW, 'Balance:', Fore.WHITE, str(balance_str), end='\r', flush=True)
        z += 1
        
        if int(balance) > 0:
            print('Winning', Fore.GREEN, str(w), Fore.WHITE, str(z), Fore.YELLOW, 'Total Scan Checking ----- BTC Address =', Fore.GREEN, str(addr), end='\r')
            w += 1
            z += 1
            f = open("winner.txt", "a")
            f.write('\nAddress = ' + str(addr))
            f.write('\nP2SH Address = ' + str(p2sh_address))
            f.write('\nP2WPKH Address = ' + str(p2wpkh_address))
            f.write('\nP2WPKH in P2SH Address = ' + str(p2wpkh_in_p2sh_address))
            f.write('\nP2WSH Address = ' + str(p2wsh_address))
            f.write('\nP2WSH in P2SH Address = ' + str(p2wsh_in_p2sh_address))
            f.write('\nPrivate Key = ' + str(private_key))
            f.write('\nMnemonic Phrase = ' + str(mnemonic))
            f.write('\n=========================================================\n')
            f.close()
            print('Winner information Saved On text file = ADDRESS ', str(addr))
            continue
        
finder(r)

if __name__ == '__main__':
    jobs = []
    for r in range(cores):
        p = multiprocessing.Process(target=finder, args=(r,))
        jobs.append(p)
        p.start()