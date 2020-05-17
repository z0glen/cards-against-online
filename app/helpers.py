import requests


def get_json(url):
    r = requests.get(url)
    print(r.json())
    return r.json()


def read_file(path):
    f = open(path, "r")
    contents = f.read()
    return contents
