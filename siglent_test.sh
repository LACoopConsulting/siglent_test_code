#!/bin/bash

COUNT=0

while true
do
	python siglent.py
	COUNT=$((COUNT+1))
	echo "Count = ${COUNT}"
done
