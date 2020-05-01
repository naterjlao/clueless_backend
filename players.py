#!/usr/bin/python3
################################################################################
# File:            players.py
# Subcomponent:    Clueless/Backend
# Language:        python3
# Author:          Nate Lao (nlao1@jh.edu)
# Date Created:    5/1/2020
# Description:
#			Contains the player related class declarations for Clueless.
#
################################################################################

from utils import *
from globals import *

# Defines a Player object
class Player:
	# A player has an ID and an assocatied suspect character.
	# A player also holds a hand of cards, a checklist used
	# for identifying suspects and a message that would 
	# be displayed to the UI
	def __init__(self,playerId,logger):
		self.logger = logger
		self.playerId = playerId
		self.suspect = None
		self.message = None
		self.cards = []
		self.checklist = []
		self.state = "IN_PLAY" # "WIN", "LOSE"
		self.logger.log("Added player %s" % playerId)
	
	def __str__(self):
		return "%s : %s" % (str(self.playerId), str(self.suspect))
	
	# Returns the ID of a player
	def getID(self):
		return self.playerId
	
	# Returns the suspect name of a player
	def getSuspect(self):
		return self.suspect
		
	# Adds a card to the Player's hand
	# The number of cards given to player is dependent on the number of players
	# in the game. This is because the cards are equally dispersed once the
	# case file is created. The types of cards the player has does not matter.
	def addCard(self,card):
		self.logger.log("Adding %s card to %s's hand" %(card,self.playerId))
		self.cards.append(card)
		
	# returns a Dictionary that comprises the Player's state to be sent
	# the client UI handler.
	def getState(self):
		return {
			"playerId"          : self.playerId,
			"suspect"           : self.suspect,
			"isSuggestionValid" : self.isSuggestionValid()
		}
	
	# Returns a list of strings where the player may go to
	# at the current position
	def getMoveOption(self):
		pass # TODO
	
	# Returns True if the Player is eligible to make a suggestion
	def isSuggestionValid(self):
		return False # TODO review the requirements for the game at the target state
		
	# Associates a suspect string name to this player
	# Note: we assume that the selection is good.
	# (ie. the player cannot select a suspect that is already choosen
	def selectSuspect(self,suspect):
		self.logger.log("Assigning %s to %s" % (suspect,self.playerId))
		self.suspect = suspect

# Wrapper for holding the list of Players registered in the game
# In addition, a list of characters that are available are stored
# in this class.
class PlayerList:
	def __init__(self,logger):
		self.logger = logger
		self.players = []
		self.availableCharacters = []
		for suspect in SUSPECTS:
			self.availableCharacters.append(suspect)
	
	def __str__(self):
		ret = ""
		for player in self.players:
			ret += str(player)
			ret += "\n"
		return ret
	
	# Adds a Player to the PlayerList with playerId
	# If the player already exists, return False else True
	def addPlayer(self,playerId):
		ret = False
		if self.getPlayer(playerId) == None:
			self.players.append(Player(playerId,self.logger))
			ret = True
		else:
			self.logger.log("Cannot add %s, player already exists" % playerId)
		return ret
	
	def getPlayers(self):
		return self.players
	
	# Returns a list of strings that represent the suspects
	# that are available to be selected
	def getAvailableCharacters(self):
		return self.availableCharacters
	
	# Returns the Player object based on playerId string
	def getPlayer(self,playerId):
		target = None
		for player in self.players:
			if player.playerId == playerId:
				target = player
		return target

	# Returns a list of dictionaries that contain the state of
	# every player
	def getPlayerstates(self):
		ret = []
		for player in self.players:
			ret.append(player.getState())
		return ret

	# Returns a list of dictionaries that contain the:
	# -playerId : <string>
	# -options: <list of strings>
	def getMoveOptions(self):
		ret = []
		for player in self.players:
			ret.append(player.getMoveOption())
		return ret

	# Returns the Player object that has the suspect name,
	# If no Player could be found, None is returned
	def getPlayerBySuspect(self,suspect):
		ret = None
		for player in self.players:
			if player.getSuspect() == suspect:
				ret = player
				break
		return ret

	# Removes the player from the playerlist and returns the player object
	def removePlayer(self,playerId):
		target = self.getPlayer(playerId)
		self.logger.log("Removing player %s" % playerId)
		self.players.remove(target)
		return target

	# Assigns the suspect to the player. If the suspect is already assigned
	# a GameError is thrown.
	def selectPlayerSuspect(self,playerId,suspect):
		player = self.getPlayer(playerId)
		# verify if the suspect has already been picked
		if suspect not in self.availableCharacters:
			raise GameError(playerId,("%s has already been picked" % suspect))
		elif suspect in SUSPECTS:
			player.selectSuspect(suspect) 				# Assign the player to the suspect
			self.availableCharacters.remove(suspect)	# Remove the suspect from the list of available characters
			self.logger.log("Available characters: %s" % (self.availableCharacters))
		else:
			raise GameError(playerId,("%s is not a suspect name" % suspect))
