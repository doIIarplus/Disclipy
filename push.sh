#!/usr/bin/env bash

autopep8 --in-place --max-line-length 90 --aggressive --aggressive --ignore=E711,E712,E713,E714 -v *.py

if [ $# -gt 0 ]; then
	git add "$@" 
else
	git add .
