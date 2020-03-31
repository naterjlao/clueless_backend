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

# Spinup a listener, this will be killed when the Serverside application is killed
while True:
	# Wait for input from the Serverside application
	data = input()
	
	# Write out to log file what occurred
	log.write("recieved %s" % data)
	log.write
	
	# Send a confirmation to the Serverside that the message was recieved
	print("message recieved", flush=True)
	
