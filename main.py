#!/usr/bin/python3
##############################################################################
# File: main.py
# Author: Nate Lao (nlao1@jh.edu)
# Created On: 3/30/2020
# Description:
#       Backend MAIN listener script for Clueless.
##############################################################################

# Open up a log file in a specified place
LOG = "/opt/clueless/log/backend.log"
log = open(LOG,'a+')
log.write('Skeletal Demo Backend Log\n')
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
    if data == "left":
        x = x - SPEED
    elif data == "right":
        x = x + SPEED
    elif data == "up":
        y = y - SPEED
    elif data == "down":
        y = y + SPEED
    
    # Write out to log file what occurred
    log.write("recieved %s\n" % data)
    #log.write("updating x -> %d\n" % x) # NOTE: disabled for demo
    #log.write("updating y -> %d\n" % y)
    log.flush()
    
    # Send data back to the Serverside -- MUST BE JSON
    returnMsg = "{\"x\":%d,\"y\":%d}" % (x,y)
    log.write("sending %s\n" % returnMsg)
    print(returnMsg, flush=True)
    
