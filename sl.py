import requests

import json


payload = {'key': '3cccb4dc80567abac4c56143b3f05cae', 'S': 'gubbangen',"Z": "slussen"}

r = requests.get("https://api.trafiklab.se/sl/reseplanerare.json", params=payload)

print json.dumps(r.json(), indent=2)
#https://api.trafiklab.se/sl/reseplanerare.xml?key=<DIN API NYCKEL>&S=9506&Z=9526&time=9:15