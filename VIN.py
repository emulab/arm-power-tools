# Records the voltage (in volts) on the cartridge
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

VIN_cmd = "ipmi-raw --no-probing --driver-type=SSIF --driver-address=0x10 --driver-device=/dev/i2c-0 0 6 0x52 0x05 0x40 0x02 0x88"
VIN_proc = subprocess.Popen(VIN_cmd.split(), stdout=subprocess.PIPE)
VIN_raw = VIN_proc.communicate()[0]
VIN_str = str(filter(None, VIN_raw)).rstrip()
record += ",VIN," + VIN_str

re_flag = re_test.match(VIN_str)
if re_flag:
  # switch two last hex pairs in order
  VIN_list = VIN_str.split(' ')
  VIN_hex = str(VIN_list[4])+ str(VIN_list[3])
  # conversion to volts
  VIN = int(VIN_hex,16) * 0.005208
  record += "," + str(VIN)
else:
  record += ",VIN_OUTPUT_FORMAT_ERROR"

print record
