import datetime
import json
import os
import re
import play_scraper
from github import Github

# define stuff
json_data = {}
json_data["KretaUserAgent"] = ""

# scrape data
play_ver = play_scraper.details('hu.eKreta.KretaAndroid')['current_version']
print("KRETA current Google Play version: " + str(play_ver))

# load existing file
file = open("./settings.json", "r")
data = file.read()
json_data = json.loads(data)
file.close()

# fetch github stuff
g = Github()
repo = g.get_repo("filcnaplo/filcnaplo")
releases = repo.get_releases()

# update stuff
json_data["LastUpdated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
json_data["LatestVersion"] = releases[0].tag_name

# write it to disk
with open('./settings.json', 'w') as outfile:
    json.dump(json_data, outfile)
