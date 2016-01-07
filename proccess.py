import os
import string
import argparse

def load(filename):
  try:
    f = open(filename, 'r')
  except IOError:
    print 'Cannot open ', filename
    exit(1)
  else:
    lines=[]
    for l in f:
      lines.append(l)
    f.close()
    return lines

def save(filename, trace):
  try:
    f = open(filename, 'w')
  except IOError:
    print 'Cannot open ', filename
    exit(1)
  else:
    for s in trace:
      f.write(s+"\n")
    f.close()

def estimate_power(raw):
  # Find the first voltage
  volt = 0
  for s in raw:
    x=s.split(",")
    cmd=x[3]
    if cmd=="VIN":
      volt = float(x[5])
      break
  # Calculated power estimates
  res = []
  for s in raw:
    x=s.split(",")
    cmd=x[3]
    if cmd=="VIN":
      volt = float(x[5])
    elif cmd == "IOUT":
      epoch=float(x[0])
      curr = float(x[5])
      p = curr * volt;

  # Old way:
  #    res.append(s.rstrip() + "," + str(volt) + "," + str(p))
  # res will contain records like this:
  #   1443894438.04,2015-10-03 17:47:18.043701,ms0128.utah.cloudlab.us,IOUT,rcvd: 52 00 08 09,3.27398,12.327336,40.3594515173
  #   1443894440.28,2015-10-03 17:47:20.283455,ms0128.utah.cloudlab.us,IOUT,rcvd: 52 00 08 09,3.27398,12.327336,40.3594515173
  #   ...
  # Last three columns: current, voltage, power

  # New way:
      res.append(x[2]+","+x[1]+","+str(p))

  return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help="File with on-node samples")
    parser.add_argument("--output", help="Result of processing")
    args = parser.parse_args()

    raw = load(args.input)
    trace = estimate_power(raw)
    save(args.output, trace)
