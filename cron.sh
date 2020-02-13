#!/bin/bash

cd /home/<homedir>/kreta;
torify python3 schoolUpdater.py;
python3.8 versionChecker.py;

cd /var/www/filcnaplo.hu/
git pull;