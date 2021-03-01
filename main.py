import os
import base64
import requests
import const
from Utilities import fconcat, segment_download
from Product import Product
import math
import asyncio
import aiohttp

DOWNLOADS_DIRECTORY = ""


def get_aliases():
    resp = requests.get(const.WR_ALIAS)
    return resp.json()


def saveContent(name, content):
    if not os.path.exists('./' + name):
        f = open('./' + name, 'wb+')
        f.write(content)
        f.close()


async def getpieces(digests, current_product, fold):
    async with aiohttp.ClientSession() as session:
        sz = len(digests)
        i = 0
        for dig in digests:
            r = None
            hd = base64.b64decode(dig).hex()
            async with session.get(current_product.cfg.config.remote.url + hd + ".solidpiece") as resp:
                r = await resp.content.read()
            saveContent(os.path.join(fold, f"digest_{i}" + ".solidpiece"), r)
            i = i + 1
            print(f"{i}/{sz} - {math.floor((i / sz) * 100)}%")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
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

    current_product = Product(aliases[choice], choice)

    if current_product.cfg.config.remote.type == "httppiece":

        fold = os.path.join(DOWNLOADS_DIRECTORY, choice)
        os.mkdir(fold)

        meta = current_product.get_meta()
        digests = meta["pieces"]["digests"]

        loop.run_until_complete(getpieces(digests, current_product, fold))

        # Concatenate files after download
        print("Processing download...")
        fext = meta["files"][0]["name"].split('.')[1]
        # os.rmdir(fold)

        if len(meta['files']) > 1:
            fconcat(fold, fold + '.solidpartial')
            extracted = segment_download(meta, fold + '.solidpartial')
            j = 0
            os.mkdir(fold + "FINAL")
            for f in meta['files']:
                with open(os.path.join(fold + "FINAL", f['name']), "wb") as file:
                    file.write(extracted[j])

                j = j + 1
        else:
            fconcat(fold, meta['files'][0]['name'])
        print("Finshed!")

    else:
        print('Download type not supported!')
