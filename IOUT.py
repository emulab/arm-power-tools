# Records the current (in amps) on the cartridge
# Author: Dmitry Duplyakin (dmitry.duplyakin@colorado.edu)

import time
import datetime
import os
import subprocess
import re
import socket

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

# Measurement example: rcvd: 52 00 FB 39
re_test = re.compile("^rcvd: [A-Z0-9][A-Z0-9] [A-Z0-9][A-Z0-9] [A-Z0-9][A-Z0-9] [A-Z0-9][A-Z0-9]$")

record = ""
record += str(time.time())
record += "," + str(datetime.datetime.now())

record += "," + socket.getfqdn()

IOUT_cmd = "ipmi-raw --no-probing --driver-type=SSIF --driver-address=0x10 --driver-device=/dev/i2c-0 0 6 0x52 0x05 0x40 0x02 0x8C"
IOUT_proc = subprocess.Popen(IOUT_cmd.split(), stdout=subprocess.PIPE)
IOUT_raw = IOUT_proc.communicate()[0]
IOUT_str = str(filter(None, IOUT_raw)).rstrip()
record += ",IOUT," + IOUT_str

re_flag = re_test.match(IOUT_str)
if re_flag:
  # switch two last hex pairs in order
  IOUT_list = IOUT_str.split(' ')
  IOUT_hex = str(IOUT_list[4])+ str(IOUT_list[3])
  # conversion to amps
  IOUT = int(IOUT_hex,16) * 0.01239 - 25.3717 
  record += "," + str(IOUT)
else:
  record += ",IOUT_OUTPUT_FORMAT_ERROR"

print record
