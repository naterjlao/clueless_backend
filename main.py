#!/usr/bin/python3
##############################################################################
# File: main.py
# Author: Nate Lao (nlao1@jh.edu)
# Created On: 3/30/2020
# Description:
#       Backend MAIN listener script for Clueless.
##############################################################################

# Open up a log file in a specified place
LOG="/opt/clueless/log/backend.log"
log = open(LOG,'w')
log.write('Skeletal Demo Backend Log')
log.flush()

# Create variables that is stored at runtime for this process
x = 200
y = 200
SPEED = 5

# Spinup a listener, this will be killed when the Serverside application is killed
while True:
    # Wait for input from the Serverside application
    data = input()
    data = data.strip()
    
    # Determine what to do with that data
    switch (data) {
        case "left":
            x = x - SPEED
            break
        case "right":
            x = x + SPEED
            break
        case "up":
            y = y - SPEED
            break
        case "down":
            y = y + SPEED
            break
    }
    
    # Write out to log file what occurred
    log.write("recieved %s" % data)
    log.write("updating x -> $d" % x)
    log.write("updating y -> $d" % y)
    log.flush()
    
    # Send data back to the Serverside -- MUST BE JSON
    print(("{x:%d,y:%d}" % x,y), flush=True)
    
