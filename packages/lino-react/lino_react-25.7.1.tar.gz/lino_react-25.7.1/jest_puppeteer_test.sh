#!/usr/bin/env bash

if [ "$1" != "skipprep" ] ; then
	python puppeteers/avanti/manage.py prep --noinput
	python puppeteers/noi/manage.py prep --noinput
fi

BASE_SITE=avanti npm run itest
BASE_SITE=noi npm run itest
