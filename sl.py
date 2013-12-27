import requests

import json



def read_dict_from_file(filename):
    with open(filename, "r+") as jsonfile:
        return json.loads(jsonfile.read())

settings = read_dict_from_file("api.key")

payload = {'key': settings["key"], 'S': 'gubbangen',"Z": "slussen"}

r = requests.get("https://api.trafiklab.se/sl/reseplanerare.json", params=payload)

print json.dumps(r.json(), indent=2)
#https://api.trafiklab.se/sl/reseplanerare.xml?key=<DIN API NYCKEL>&S=9506&Z=9526&time=9:15