import base64
import json
import os

def parse_response_hybrid(data:str):
    # Select B64'd Body, parse json and return
    body = base64.b64decode(data.split('.')[1]+"===")
    return json.loads(body)

def fconcat(fldr, output):
    filenames = os.listdir(fldr)
    filenames.sort(key=lambda fname: int(''.join(filter(str.isdigit, fname))))

    with open(output,'wb+') as out:
        for f in filenames:
            i = open(os.path.join(fldr,f),'rb')
            out.write(i.read())
            i.close()
