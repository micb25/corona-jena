#!/bin/bash

# Thuringia
TMPFILE=`mktemp`
./crawler_thuringia.py > /dev/null
cat ../data/cases_thuringia.csv | sort | uniq > $TMPFILE
mv $TMPFILE ../data/cases_thuringia.csv
chown 10006:10006 ../data/cases_thuringia.csv
chmod go+r ../data/cases_thuringia.csv

