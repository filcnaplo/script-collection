#!/bin/bash

cd /home/marci/kreta;
python3 school_list.py;
python3 settings.py;

cd /var/www/filcnaplo.hu/
git pull;
