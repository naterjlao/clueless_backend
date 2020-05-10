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
			print(msg)
		else:
			self.file.write("%s\n" % msg)
			# TODO append the message
			# TODO push to log file

# Custom error and exception classes

# These exceptions are logically invalid and shouldn't be possible
# for triggering. These should only be used to sanity check the logic
# of the game itself, rather than player actions.
# TLDR; these are fuckup checks for me (nate)
class BackException(Exception):
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return self.msg

# These exceptions are triggered by errors caused by the player.
# These are caught within the signal handlers for each player actions.
# These should only be raised by the player is trying to perform
# an action that is against the game rules. When this is caught,
# the player's message attributes are reset to default.
# Note that two arguments must be provided:
# - The player object or "all"
# - The error message to be displayed to the player
class GameException(Exception):
	def __init__(self,player, msg):
		self.player = player
		self.msg = msg
	def __str__(self):
		return "%s: %s" % (self.player,self.msg)
