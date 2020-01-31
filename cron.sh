#!/bin/bash

WORKDIR="/tmp/workdir"
APKDIR="$WORKDIR/Raccoon/content/apps/hu.eKreta.KretaAndroid/"

cd "$WORKDIR"
# update school list through tor
torsocks python3 schoolUpdater.py

# delete the old download
echo "deleting $APKDIR ..."
rm -rf "$APKDIR";

# check for current version
CURRENTVER=$(python3 versionChecker.py)

# compare the two versions
OLDVER=$(sqlite3 database.db "select kreta_ver from settings")
echo "versions (old v new): $OLDVER - $CURRENTVER"
sqlite3 database.db "update settings set kreta_ver='$CURRENTVER'"

# decide if update is needed
if [ "$OLDVER" == "$CURRENTVER" ]; then
    echo "update not needed"
    python3 finalizeScript.py "nofullupdate";
    exit;
fi

# run the downloader
java -jar "raccoon-4.10.0.jar" --gpa-download "hu.eKreta.KretaAndroid";

# getting apk filepath
FILE=$(find $APKDIR -type f -name "*.apk" | head -n 1)
echo "apk is at $FILE"

# check if file is downloaded or not
if [ -f $FILE ]; then

    # run the finalizing script
    echo "running finalizing script"
    python3 finalizeScript.py "$FILE";

    # clean up
    echo "cleaning up..."
    rm -rf "$APKDIR";
    rm -rf ./hu.eKreta.KretaAndroid*

else
    echo "download failed"
fi
