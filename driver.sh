#!/bin/bash

DIR=/var/log/power
mkdir $DIR
LOG=$DIR/`hostname -f`.log

while :
do
  python IOUT.py >> $LOG 2>&1
  sleep 1
  python VIN.py >> $LOG 2>&1
  sleep 1
done
