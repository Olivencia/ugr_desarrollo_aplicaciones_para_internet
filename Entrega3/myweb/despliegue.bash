#!/bin/bash

if [ $1 == "on" ]; then
	cp "myweb/settings.py.prod" "myweb/settings.py"
	cp -r static/* /var/www/static/
	echo "MODO PRODUCCION"

elif [ $1 == "off" ]; then
	cp "myweb/settings.py.dev" "myweb/settings.py"
 	echo "MODO DESARROLLO"
 fi