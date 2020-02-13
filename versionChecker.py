import play_scraper
import datetime
import sqlite3
import json
import os
import re

def create_connection(db_file):
	connection = None
	try:
		connection = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return connection

def query(connection, string):
	cur = connection.cursor()
	cur.execute(string)
	rows = cur.fetchall()
	return rows

user_agent = ""
json_data = ""
dbFile = "./database.file"
full_play_ver = play_scraper.details('hu.eKreta.KretaAndroid')['current_version']
play_ver = int(full_play_ver.replace(".", ""))
connection = create_connection(dbFile)
full_filc_ver = str(query(connection, "SELECT filc FROM settings WHERE 1")[0][0])
kreta_ver = int(query(connection, "SELECT kreta FROM settings WHERE 1")[0][0].replace(".", ""))

if (play_ver > kreta_ver):
	os.system("cd PlaystoreDownloader; python3.8 download.py hu.eKreta.KretaAndroid")
	os.system("cd PlaystoreDownloader/Downloads; apktool d *.apk")
	output = os.popen("cat PlaystoreDownloader/Downloads/*/apktool.yml | grep versionCode").read()
	os.system("rm -rf PlaystoreDownloader/Downloads/*")
	version_code = re.findall("(?<=')(.*)(?=')", output)[0]
	user_agent = "Kreta.Ellenorzo/" + full_play_ver + "." + version_code + " " + "(Android; <codename> 0.0)"
	query(connection, 'update settings set kreta="' + str(play_ver) + '" where 1;')
	connection.commit()


file = open("./settings.json", "r")
data = file.read()
json_data = json.loads(data)

json_data["LatestVersion"] = full_filc_ver

if (len(user_agent) > 1):
	json_data["KretaUserAgent"] = user_agent


json_data["LastUpdated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

file.close()
with open('./settings.json', 'w') as outfile:
    json.dump(json_data, outfile)
