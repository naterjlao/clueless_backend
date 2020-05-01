#!/usr/bin/python3
################################################################################
# File:            utils.py
# Subcomponent:    Clueless/Backend
# Language:        python3
# Author:          Nate Lao (nlao1@jh.edu)
# Date Created:    4/28/2020
# Description:
#			Contains the utility class declarations for Clueless.
#
################################################################################			
from globals import *

# Define and initialize a logger object.
# There will be only one logger for each python file.
# Log files will be pushed to /opt/clueless/log/backend.log
class Logger:
	# TODO remove init, not needed
	def __init__(self):
		if not DEBUG:
			self.file = open(LOG_FILE,'w+')
	def log(self,msg):
		if DEBUG:
			pass
			#print(msg)
		else:
			pass
			# TODO find the timestamp
			# TODO append the message
			# TODO push to log file

# Custom error and exception classes
class BackException(Exception):
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return self.msg


class GameError(Exception):
	def __init__(self,playerId, msg):
		self.playerId = playerId
		self.msg = msg
	def __str__(self):
		return "%s: %s" % (self.playerId,self.msg)
