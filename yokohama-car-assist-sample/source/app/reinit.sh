#!/bin/bash

rm db.sqlite3
find -name "0001_initial.py" -exec rm {} \;
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createdefaultsuperuser
python3 manage.py loaddata ec/fixtures/seeder.json
