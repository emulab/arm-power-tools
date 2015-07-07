# Records the CPU Core power via the 0x20 register
# Author: Dmitry Duplyakin (dmitry.duplyakin@colorado.edu)

import time
import datetime
import os
import subprocess
import re
import socket

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

record = ""
record += str(time.time())
record += "," + str(datetime.datetime.now())

record += "," + socket.getfqdn()

CPU_cmd = "ipmi-raw --no-probing --driver-type=SSIF --driver-address=0x10 --driver-device=/dev/i2c-0 0 6 0x52 0x05 0x8e 0x02 0x20"
CPU_proc = subprocess.Popen(CPU_cmd.split(), stdout=subprocess.PIPE)
CPU_raw = CPU_proc.communicate()[0]
CPU_str = str(filter(None, CPU_raw)).rstrip()
record += ",CPU," + CPU_str

print record
