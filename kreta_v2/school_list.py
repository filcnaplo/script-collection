import requests
import json

# config #
fileName = "school_list.json"
url = "https://kretaglobalmobileapi2.ekreta.hu/api/v3/Institute"
apiKey = "7856d350-1fda-45f5-822d-e1a2f3f1acf0"
userAgent = "hu.ekreta.student/0/Android"
##########

customHeaders = {
	"User-Agent": userAgent,
	"apiKey": apiKey
}

r = requests.get(url, headers=customHeaders)

if r.status_code == 200:
	data = json.loads(r.text.replace("\\r\\n", ""))

	for element in data:
		element.pop("advertisingUrl")
		element.pop("informationImageUrl")
		element.pop("informationUrl")
		element.pop("featureToggleSet")
		element.pop("url")
		element.pop("instituteId")

	output = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

	outFile = open(fileName, 'w')
	outFile.write(output)
	outFile.close()

else:
	print("Error: request got" + str(r.status_code))
