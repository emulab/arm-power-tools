# Records the SoC power via the 0x21 register 
# According to Mik (HP): 0x21 (reports SoC Power - everything but core, like DDR and miscellaneous IO)
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

SOC_cmd = "ipmi-raw --no-probing --driver-type=SSIF --driver-address=0x10 --driver-device=/dev/i2c-0 0 6 0x52 0x05 0x8e 0x02 0x21"
SOC_proc = subprocess.Popen(SOC_cmd.split(), stdout=subprocess.PIPE)
SOC_raw = SOC_proc.communicate()[0]
SOC_str = str(filter(None, SOC_raw)).rstrip()
record += ",SOC," + SOC_str

print record
