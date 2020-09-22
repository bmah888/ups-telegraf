#! /usr/bin/env python

import sys
import subprocess

ups_name="ups" # default value
upsc_command="upsc"
measurement_name="ups"

# Command-line parsing.  There is one optional argument, the name of
# the UPS to query.
if len(sys.argv) > 1:
    ups_name=sys.argv[1]

cmd=upsc_command + " " + ups_name

output=""
string_measurements=["battery.mfr.date", "battery.type", "device.mfr", "device.model","device.serial","device.type",
			"driver.name", "driver.parameter.port", "driver.parameter.synchronous", "driver.version", "driver.version.data", "driver.version.internal",
			"ups.beeper.status", "ups.mfr","ups.model", "ups.productid", "ups.serial", "ups.status", "ups.test.result", "ups.vendorid"]

p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

for line in p.stdout.readlines(): #read and store result in log file
    line = line.decode("utf-8").rstrip()
    key = line[:line.find(":")]
    value = line[line.find(":")+2:]

    # Determine whether a given value should be treated as a string.
    # If the key is included in string_measurements, we treat as a
    # string regardless.  Otherwise, see if a conversion to an
    # integer or a float can succeed...if not we assume a string.
    stringify = False
    if key in string_measurements:
        stringify = True
    else:
        try:
            val = int(value)
        except ValueError:
            try:
                val = float(value)
            except ValueError:
                stringify = True

    if stringify:
        value = '"' + value + '"'
    measurement = key + "=" + value
    if output != "":
        measurement = "," + measurement
    output += measurement

output = measurement_name + ",ups=" + ups_name + " " + output.rstrip()
print(output, end='')

