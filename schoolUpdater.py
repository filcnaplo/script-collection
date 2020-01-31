import requests
import json
import sys

outfile = "./schoolfile.json"

r = requests.get('https://kretaglobalmobileapi.ekreta.hu/api/v1/Institute', 
	headers={"apiKey" : "7856d350-1fda-45f5-822d-e1a2f3f1acf0"})

response = json.loads(r.text)

for item in response:
	item.pop("AdvertisingUrl")

response = json.dumps(response, sort_keys=True, ensure_ascii=False)

schoolFile = open(outfile, 'w')
schoolFile.write(response)
schoolFile.close()