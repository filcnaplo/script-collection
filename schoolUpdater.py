import requests
import json
import sys

r = requests.get('https://kretaglobalmobileapi.ekreta.hu/api/v1/Institute', 
	headers={"apiKey" : "7856d350-1fda-45f5-822d-e1a2f3f1acf0"})

response = json.loads(r.text)

for item in response:
	item.pop("AdvertisingUrl")

response = json.dumps(response, sort_keys=True, ensure_ascii=False)

schoolFile = open('./school_list.json', 'w')
schoolFile.write(response)
schoolFile.close()
