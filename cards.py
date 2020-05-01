#!/usr/bin/python3
################################################################################
# File:            cards.py
# Subcomponent:    Clueless/Backend
# Language:        python3
# Author:          Nate Lao (nlao1@jh.edu)
# Date Created:    5/1/2020
# Description:
#			Contains the card related class declarations for Clueless.
#
################################################################################

from utils import *
from globals import *
	
# Defines a Card object
# A card may either be a:
# - suspect
# - room
# - weapon
class Card:
	def __init__(self,name,logger):
		self.logger = logger
		self.name = name
	
	def __str__(self):
		return str(self.name)

	# Returns True if the card is SUSPECT type
	def isSuspect(self):
		return self.name in SUSPECTS
	
	# Returns True if the card is WEAPON type
	def isWeapon(self):
		return self.name in WEAPONS
		
	# Returns True if the card is ROOM type
	def isRoom(self):
		return self.name in ROOMS
		

# Manages all cards that are held in the game
# Information concerning the location of any
# card is stored in this object.
# There shall always be one CardManager in a Game
# instance.
# Cards are stored in dictionary that contain:
# key: the name of the card
# value: either
#     - the <playerId> of the person holding the card
#     - "UNASSIGNED"
#     - "CASE_FILE"
#
class CardManager:
	# Generates the cards based on the global CARDS 
	# All card are unassigned initially
	def __init__(self,logger):
		self.logger = logger
		self.cards = {}
		for card in CARDS:
			self.cards[card] = "UNASSIGNED"
	
	# From the given PlayerList object and CaseFile
	# The CardManager randomly chooses three cards from the
	# deck to place in the case file
	def assign(self,playerlist):
		pass # TODO
		
# Defines the CaseFile object in the game.
# There shall only be one CaseFile per instance of a game.
# The values assigned during initialization MUST NOT BE CHANGED
# The CaseFile must contain 1 card from each type:
# - suspect
# - weapon
# - room
class CaseFile:
	def __init__(self,suspectCard,roomCard,weaponCard,logger):
		self.logger = logger
		self.suspectCard = suspectCard
		self.weaponCard = weaponCard
		self.roomCard = roomCard

	# Returns True if the accusation suspect, room and weapon
	# matches the values set in the case file.
	# False otherwise.
	def checkAccusation(self,suspect, room, weapon):
		ret = True
		if (self.suspectCard.name != suspect):
			ret = False
		if (self.weaponCard.name  != weapon):
			ret = False
		if (self.roomCard.name    != room):
			ret = False
		return ret
