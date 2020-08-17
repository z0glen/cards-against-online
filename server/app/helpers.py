import requests
import json


def get_json(url):
    r = requests.get(url)
    print(r.json())
    return r.json()


def read_file(path):
    f = open(path, "r")
    contents = f.read()
    f.close()
    return json.loads(contents)


def join_cards():
    calls = read_file('calls.json')
    f = open('joined_cards.txt', "w")
    for c in calls:
        f.write("%s\n" % '_____'.join(c['text']))
    f.write("\n\n")
    responses = read_file('responses.json')
    for r in responses:
        f.write("%s\n" % '_____'.join(r['text']))
    f.close()
