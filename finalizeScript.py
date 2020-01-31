import re
import json
import datetime
import sqlite3
import random
import sys

result = ""
fullUpdate = True
filePath = './settings.json' 

conn = sqlite3.connect('database.db')
c = conn.cursor()

if sys.argv[1] == "nofullupdate":
	fullUpdate = False
	print("no full update")
if fullUpdate:
	print("full update")
	print(sys.argv[1])
	numbers = re.findall(r'\b\d+\b', sys.argv[1])
	print(numbers)
	c.execute("select kreta_ver from settings where 1")
	kretaVer = c.fetchall()[0]
	result = "Kreta.Ellenorzo/" + ''.join(kretaVer) + "." + ''.join(numbers) + " (Android; <codename> 0.0)"

else:
	tempFile = open(filePath, 'r')
	oldJson = json.loads(tempFile.read())
	result = oldJson["FillableUserAgent"]
	tempFile.close()

c.execute("select filc_ver from settings where 1")
version = c.fetchall()[0]
version = re.sub("[^0-9.]", "", str(version))
conn.close()

jsonData = {
        "LatestVersion" : version,
        "KretaUserAgent": result,
        "LastUpdated": str(datetime.datetime.now()),
}

final = json.dumps(jsonData, sort_keys=True)
print(final)

finalFile = open(filePath, 'w')
finalFile.write(final)
finalFile.close()
