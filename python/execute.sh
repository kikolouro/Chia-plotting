#!/bin/bash


#gunicorn main:app --reload
gunicorn --chdir api main:app --threads 2 --reload 
#-b 0.0.0.0:5000