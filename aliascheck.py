import requests
import json
import re
from Utilities import parse_response_hybrid

url = "https://d2sm7pvcpl7kby.cloudfront.net/aliases.json"
url2 = "https://files.wolframcdn.com/pub/RE/Mathematica/"

def parsekey(key):
    regex = r"^Payload\.M-(OSX|WIN)?-([A-Z]+)-([0-9]+\.+[0-9]+\.[0-9])-([0-9]+)\.([0-9]+)"

    matches = re.finditer(regex, key, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):

        # print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
        #                                                                     end=match.end(), match=match.group()))
        return match.groups()

if __name__ == '__main__':

    resp = requests.get(url).json()

    # tup = parsekey("Payload.M-WIN-L-12.2.0-7066604.2020081733")
    # print(tup)
    for key, val in resp.items():
        # print("")
        tup = parsekey(key)

        if tup is None:
            print(f"{key} --> {val} | UNKNOWN")
            continue

        opsys, prod, ver, build, date = tup

        resp = requests.get(url2+ver+".0/"+val+"/catalog.json")

        if resp.status_code == 404:
            print(f"{key} --> {val} | FAIL")
        elif resp.status_code == 200:
            print(f"{key} --> {val} | SUCCESS")


