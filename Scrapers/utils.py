import requests
import hashlib
from bs4 import BeautifulSoup
import json

class Entity:
    def __init__(self):
        self.__data = {}
    
    def getData(self, key=None):
        if key is None:
            return self.__data
        return self.__data[key]
    
    def setData(self, key, value):
        self.__data.update({ key: value })

    def export(self):
        def recursiveRead(x):
            if type(x) != dict and type(x) != list and not isinstance(x, Entity):
                return x

            data = x
            if isinstance(x, Entity):
                data = x.getData()
            
            if type(data) == list:
                for i in range(len(data)):
                    data[i] = recursiveRead(data[i])
            elif type(data) == dict:
                for key in data:
                    data[key] = recursiveRead(data[key])

            return data

        return recursiveRead(self.__data)

def memoized(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func


get = memoized(lambda url: BeautifulSoup(requests.get(url).text, "html.parser"))
hash = lambda prefix,string: str(int(hashlib.blake2s((prefix + string).encode('utf-8'), digest_size=8).hexdigest(),16))
hashBatch = lambda prefix,L: [hash(prefix,x) for x in L if isinstance(x,str)]

# def get(url):
#     res = requests.get(url, stream=True)
#     res.raw.decode_content = True
#     return BeautifulSoup(res.raw, "html.parser")

@memoized
def getPageTitle(url):
    return get(url).title.string

def saveAsJson(json_obj, filename):
    with open(filename, 'w') as f:
        json.dump(json_obj, f, indent=2)

    print(f"-> File saved: {filename}\n")

def downloadIcon(url, savePath):
    with open(savePath, 'wb') as f:
        fileContent = requests.get(url, params={'downloadformat': 'png'}).content
        f.write(fileContent)

def downloadCard(url, savePath):
    with open(savePath, 'wb') as f:
        fileContent = requests.get(url, params={'downloadformat': 'png'}).content
        f.write(fileContent)