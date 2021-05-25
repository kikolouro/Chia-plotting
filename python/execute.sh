#!/bin/bash


#gunicorn main:app --reload
cd ./api
gunicorn main:app --reload --timeout 1000 --bind 0.0.0.0:5000
#