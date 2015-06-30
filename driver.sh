#!/bin/bash

LOG=/var/log/power.log

while :
do
  python IOUT.py >> $LOG 2>&1
  sleep 1
  python VIN.py >> $LOG 2>&1
  sleep 1
done
