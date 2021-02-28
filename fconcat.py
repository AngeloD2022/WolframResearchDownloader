import os

def fconcat(fldr, output):
    filenames = os.listdir(fldr)
    filenames.sort(key=lambda fname: int(''.join(filter(str.isdigit, fname))))

    with open(output,'wb+') as out:
        for f in filenames:
            i = open(os.path.join(fldr,f),'rb')
            out.write(i.read())
            i.close()



