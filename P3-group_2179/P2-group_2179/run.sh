#!/bin/sh
source venv/bin/activate
python3 restify/manage.py makemigrations
python3 restify/manage.py migrate
python3 restify/manage.py runserver