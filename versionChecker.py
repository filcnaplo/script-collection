from github import Github
import play_scraper
import datetime
import json
import os
import re

# set variables
user_agent = ""
json_data = ""
play_ver = play_scraper.details('hu.eKreta.KretaAndroid')['current_version']
kreta_ver = open("./kreta_version.txt", "r").read()

# run other scripts if there was an update
if (play_ver != kreta_ver):
	os.system("cd PlaystoreDownloader; python3.8 download.py hu.eKreta.KretaAndroid")
	os.system("cd PlaystoreDownloader/Downloads; apktool d *.apk")
	output = os.popen("cat PlaystoreDownloader/Downloads/*/apktool.yml | grep versionCode").read()
	os.system("rm -rf PlaystoreDownloader/Downloads/*")
	version_code = re.findall("(?<=')(.*)(?=')", output)[0]
	user_agent = "Kreta.Ellenorzo/" + play_ver + "." + version_code + " " + "(Android; <codename> 0.0)"

# update kreta_version.txt
file = open("./kreta_version.txt", "w")
file.write(play_ver)
file.close()

# read existing settings.json file into memory
file = open("./settings.json", "r")
data = file.read()
json_data = json.loads(data)
file.close()

# fetch latest version from github
g = Github()
repo = g.get_repo("filcnaplo/filcnaplo")
releases = repo.get_releases()

# check if user agent was updated
if (len(user_agent) > 1):
	json_data["KretaUserAgent"] = user_agent

# update settings.json in memory
json_data["LastUpdated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
json_data["LatestVersion"] = releases[0].title

# write it to disk
with open('./settings.json', 'w') as outfile:
    json.dump(json_data, outfile)
