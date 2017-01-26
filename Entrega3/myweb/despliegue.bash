#!/bin/bash

if [ $1 == "on" ]; then
	cp "myweb/settings.py.prod" "myweb/settings.py"
	echo "1"

elif [ $1 == "off" ]; then
	cp "myweb/settings.py.dev" "myweb/settings.py"
 	echo "2"
 fi