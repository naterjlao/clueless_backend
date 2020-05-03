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
		self.message = ""
		self.messageColor = "blue" # Setting to default for now
		self.cards = []
		self.checklist = []
		self.state = PLAYER_IN_PLAY # It is assumed that when a player is made, he's automatically thrown to in play
		self.logger.log("Added player %s" % playerId)
	
	def __str__(self):
		return "%s (%s)" % (str(self.suspect), str(self.playerId))
	
	# Returns the ID of a player
	def getID(self):
		return self.playerId
	
	# Returns the suspect name of a player
	def getSuspect(self):
		return self.suspect
		
	# Reverts message attributes to initial settings
	def resetMessage(self):
		self.message = ""
		self.message = "blue"
		
	# Returns a message string and message color tuple
	def getMessage(self):
		return self.message,self.messageColor
		
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
		return self.state == PLAYER_SUGGEST # TODO make sure this get thrown back to IN_PLAY
		
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
		self.currentPlayer = None
		self.availableCharacters = []
		for suspect in SUSPECTS:
			self.availableCharacters.append(suspect)
	
	def __str__(self):
		ret = ""
		for player in self.players:
			ret += str(player)
			ret += "\n"
		return ret
	
	# Returns true only if the current player is the given player
	def hasTurn(self,player):
		return player == self.currentPlayer
	
	# Returns the player object representing the current player who has the turn in the game
	def getCurrentPlayer(self):
		return self.currentPlayer
	
	# Picks the next player to have a turn, this is based on the SUSPECTS list
	def nextCurrentPlayer(self):
		# Determine the index of the current player in respect to the SUSPECTS list
		foundIdx = 0
		found = False
		while (foundIdx < len(SUSPECTS)) and (not found):
			# Breaks when the suspect of current player is found in the SUSPECTS list
			if (self.currentPlayer.getSuspect() == SUSPECTS[foundIdx]):
				found = True
			else:
				foundIdx += 1
		# Increment in the index and modulo if necessary
		idx = (foundIdx + 1) % len(SUSPECTS)
		candidate = None
		
		# Loop through the SUSPECTS list, the next player who has
		# a turn is based on the next character in the list
		while (idx < len(SUSPECTS)) and (candidate == None):
			# At this point, we've wrapped around around the 
			# SUSPECTS list, but we couldn't find the next player
			if idx == foundIdx:	
				raise GameError("could not find the next player based on SUSPECT list")
			else:
				# Determine if the suspect is being used by a player
				candidate = self.getPlayerBySuspect(SUSPECTS[idx])
				# Else, increment the index
				idx = (idx + 1) % len(SUSPECTS)
		
		self.logger.log("Determined the next player: %s" % str(candidate))
		self.currentPlayer = candidate
	
	# Sets up the starting player for the game
	def startGame(self):
		if len(self.players) < MIN_PLAYERS:
			raise GameError("need at least %d players to play the game, only found %d" % (MIN_PLAYERS,len(self.players)))
		elif len(self.players) > MAX_PLAYERS:
			raise GameError("need at most %d players to play the game, only found %d" % (MAX_PLAYERS,len(self.players)))
		else:
			# Find the starting player based on the order of suspects
			startPlayer = None
			idx = 0
			while (startPlayer == None) and idx < len(SUSPECTS):
				startPlayer = self.getPlayerBySuspect(SUSPECTS[idx])
				idx += 1
			self.logger.log("setting first player: %s" % startPlayer)
			self.currentPlayer = startPlayer
	
	# Adds a Player to the PlayerList with playerId
	# If a new player was added, the new Player object is returned
	# If the player already existed, None is returned
	def addPlayer(self,playerId):
		newPlayer = None
		if self.getPlayer(playerId) == None:
			newPlayer = Player(playerId,self.logger)
			self.players.append(newPlayer)
		else:
			self.logger.log("Cannot add %s, player already exists" % playerId)
		return newPlayer
	
	# Returns a list of all players in the playerlist
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

	# This must be called when the player has started the game,
	# players should no longer be able to select new characters
	def lockAvailableCharacters(self):
		self.logger.log("Available characters lockdown")
		# Blow away all available characters that can be picked
		self.availableCharacters = []

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
		if target != None: # TODO this might need to be verified
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
