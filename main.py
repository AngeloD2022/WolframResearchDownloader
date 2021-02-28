import os
import base64
import requests
import const
from Utilities import fconcat
from Product import Product
import math

DOWNLOADS_DIRECTORY = ""


def get_aliases():
    resp = requests.get(const.WR_ALIAS)
    return resp.json()


def saveContent(name, content):
    if not os.path.exists('./' + name):
        f = open('./' + name, 'wb+')
        f.write(content)
        f.close()


if __name__ == '__main__':
    print("Wolfram Research Downloader")
    print("Version 1.0.0 - Written by Angelo DeLuca")

    DOWNLOADS_DIRECTORY = os.path.join(os.path.curdir, "wrdownloads")

    if not os.path.exists(DOWNLOADS_DIRECTORY):
        print("Downloads folder not found- Creating it...")
        os.mkdir(DOWNLOADS_DIRECTORY)

    # User makes a selection from the product catalog...
    aliases = get_aliases()

    for n in aliases:
        print(n + " --> " + aliases[n])
    choice = input("Choose a product...")

    # Obtain download metadata
    print("Obtaining download information...")

    current_product = Product(aliases[choice])

    if current_product.cfg.config.remote.type == "httppiece":

        fold = os.path.join(DOWNLOADS_DIRECTORY,choice)
        os.mkdir(fold)

        meta = current_product.get_meta()
        digests = meta["pieces"]["digests"]

        sz = len(digests)
        i = 0

        for dig in digests:
            hd = base64.b64decode(dig).hex()
            r = requests.get(current_product.cfg.config.remote.url + hd +".solidpiece")
            saveContent(os.path.join(fold,f"digest_{i}"+".solidpiece"), r.content)
            i = i+1
            print(f"{i}/{sz} - {math.floor((i/sz) * 100)}%")

        # Concatenate files after download
        print("Processing download...")
        fext = meta["files"][0]["name"].split('.')[1]
        fconcat(fold,fold+'.'+fext)
        os.rmdir(fold)
        print("Finshed!")

    else:
        print('Download type not supported!')


