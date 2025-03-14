#!/bin/sh
sudo apt install python3-pip
sudo apt install python3.8-venv
python3 -m venv venv
source venv/bin/activate
pip install django
pip install djangorestframework
pip install pillow
pip install djangorestframework-simplejwt