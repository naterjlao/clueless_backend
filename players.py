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
		self.checklist = []
		self.state = PLAYER_INITIAL # It is assumed that when a player is made, he's automatically thrown to in play
		self.logger.log("Added player %s" % playerId)
	
	def __str__(self):
		return "%s (%s)" % (str(self.suspect), str(self.playerId))
	
	# Does nothing but raises a GameException if the player is not ready to play
	def validatePlayer(self):
		if self.state != PLAYER_INITIAL:
			raise GameException(self,"player %s is not in initial state" % self.playerId)
		if self.suspect == None:
			raise GameException("all","player %s does not have a suspect character" % self.playerId)
	
	# Returns the ID of a player
	def getID(self):
		return self.playerId
	
	# Returns the suspect name of a player
	def getSuspect(self):
		return self.suspect
	
	# Updates the player's personal message for UI
	def updateMessage(self,message,color="blue"):
		self.message = message
		self.color = color
	
	# Reverts message attributes to initial settings
	def resetMessage(self):
		self.message = ""
		self.messageColor = "blue"
		
	# Returns a message string and message color tuple
	def getMessage(self):
		return self.message,self.messageColor
	
	# The checklist will contain all the seen stuff in all categories,
	# will be sorted out when it needs to be returned
	def updateChecklist(self,evidence):
		if not (evidence in self.checklist):
			self.checklist.append(evidence)
		
	# Returns a dictionary object containing the suspects, weapons and rooms
	# in a player's checklist
	def getChecklist(self):
		checklist = {"suspects":[],"weapons":[],"rooms":[]}
		for evidence in self.checklist:
			if evidence in SUSPECTS:
				checklist["suspects"].append(evidence)
			
			elif evidence in WEAPONS:
				checklist["weapons"].append(evidence)
			
			elif evidence in ROOMS:
				checklist["rooms"].append(evidence)
				
		return checklist
		
	# returns a Dictionary that comprises the Player's state to be sent
	# the client UI handler.
	def getState(self):
		return {
			"playerId"          : self.playerId,
			"suspect"           : self.suspect,
			"isSuggestionValid" : self.isSuggestionValid()
		}
	
	# Returns True if the Player is eligible to make a suggestion
	def isSuggestionValid(self):
		# A player is only able to make a suggestion iff he is in a room
		# This state is handled by movement on the gameboard
		# If the player has moved to a room by his own will, he MUST make a suggestion
		# If the player was forced to a room, a suggestion is optional
		return self.state == PLAYER_SUGGEST # TODO make sure this get thrown back to IN_PLAY
	
	# Processes a suggestion request, the player is LOCKED until the suggestion is
	# satisfied. Afterwards, the player is in play and turn is incremented to the next player
	# in the cycle.
	def makeSuggestion(self):
		# The playerlist
		pass
		# Push the state to IN_PLAY
	
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
		self.currentPlayerTemp = None
		self.availableCharacters = []
		for suspect in SUSPECTS:
			self.availableCharacters.append(suspect)
	
	def __str__(self):
		ret = ""
		for player in self.players:
			ret += str(player)
			ret += "\n"
		return ret
	
	# Should be called if a valid move has been performed
	def resetMessages(self):
		for player in self.players:
			player.resetMessage()
	
	# This does nothing but raises a GameException if a player is not ready to play
	def validatePlayers(self):
		for player in self.players:
			player.validatePlayer()
	
	# Starts a suggestion round
	# Note that the player in this case is the caller player
	def makeSuggestion(self,suggestion,gameboard):
		for p in self.players:
			# Lock all players
			p.state = PLAYER_LOCKED
			
		# Get the target player
		target = self.getPlayerBySuspect(suggestion.target)
		
		# Move the target to suggestion room
		gameboard.movePlayer(target,suggestion.room,force=True)
		
		# Set the target's state to SUGGESTION DEFEND
		target.state = PLAYER_DEFEND
		# Set the turn to the target player and save the current player
		self.currentPlayerTemp = suggestion.accuser
		self.currentPlayer = target
	
	
	# Ends a suggestion round
	# Note that the player in this case is the target player
	def endSuggestion(self,player,counter,suggestion,gameboard,casefile,cannotDisprove=False):
		for p in self.players:
			p.state = PLAYER_IN_PLAY
		# pop the current player from tempCurrent and resume the game
		self.currentPlayer = self.currentPlayerTemp
		self.currentPlayerTemp = None
		
		# TODO there needs to be something here to push if the player
		# TODO cannot disprove the suggestion with the cards he has
		# TODO If this is the case, something must singal the target (accused)
		# TODO that we cannot win the case at this point.
		
		
		
		if (cannotDisprove):
			# The accused had just shown a card that disprove the suggestion.
			self.updateChecklists(suggestion.caller,counter)
		else:
			self.nextCurrentPlayer()
	
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
				raise BackException("could not find the next player based on SUSPECT list")
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
			raise GameException("all","need at least %d players to play the game, only found %d" % (MIN_PLAYERS,len(self.players)))
		elif len(self.players) > MAX_PLAYERS:
			raise GameException("all","need at most %d players to play the game, only found %d" % (MAX_PLAYERS,len(self.players)))
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
	
	# Returns a list of strings that represent the suspects
	# that were already picked in the game.
	def getCharactersInGame(self):
		characters = []
		for player in self.getPlayers():
			suspect = player.getSuspect()
			if suspect != None:
				characters.append(suspect)
		return characters
		
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
			raise GameException(playerId,("%s has already been picked" % suspect))
		elif suspect in SUSPECTS:
			player.selectSuspect(suspect) 				# Assign the player to the suspect
			self.availableCharacters.remove(suspect)	# Remove the suspect from the list of available characters
			self.logger.log("Available characters: %s" % (self.availableCharacters))
		else:
			raise GameException(playerId,("%s is not a suspect name" % suspect))



# Class definition of a suggestion object bc object oriented programming
# is supposed to make life easier by encapsulation what is a NEED TO KNOW
# versus WHAT HAPPENS UNDER THE HOOD. If a class is fucked, then we can
# at least narrow down the shit.
class Suggestion:

	# Note that all parameters MUST be strings.
	def __init__(self,accuser,suspect,weapon,room,logger):
		if suspect.__class__ != str:
			raise GameError("make sure suspect in Suggestion is a string")
		if weapon.__class__ != str:
			raise GameError("make sure weapon in Suggestion is a string")
		if room.__class__ != str:
			raise GameError("make sure room in Suggestion is a string")
			
		self.logger = logger
		self.logger.log("spawned Suggestion %s %s %s" % (suspect,weapon,room))
		
		# This is the player object that made the suggestion
		self.accuser = accuser
		
		self.suspect = suspect
		self.weapon = weapon
		self.room = room
	
	# This returns True if the Suggestion can be countered
	# False otherwise. The counter object can be either
	# a character, weapon or room. (A character because the
	# the suspect player can hold a card of himself, ergo
	# he has an alibi.)
	def counter(self,counter):
		ret = False
		if counter == self.suspect:
			ret = True
		if counter == self.weapon:
			ret = True
		if counter == self.room:
			ret = True
		return ret
	
# Class definition of an Accusation. See Suggestion.
class Accusation:
	# Note that all parameters MUST be strings.
	def __init__(self,accuser,suspect,weapon,room,logger):
		if suspect.__class__ != str:
			raise GameError("make sure suspect in Accusation is a string")
		if weapon.__class__ != str:
			raise GameError("make sure weapon in Accusation is a string")
		if room.__class__ != str:
			raise GameError("make sure room in Accusation is a string")
			
		self.logger = logger
		self.logger.log("spawned Accusation %s %s %s" % (suspect,weapon,room))
		
		# This is a player object that created the accusation
		self.accuser = accuser
		
		self.suspect = suspect
		self.weapon = weapon
		self.room = room
	
	# This returns True if the accusation can be countered
	# False otherwise. The counter object can be either
	# a character, weapon or room. (A character because the
	# the target player can hold a card of himself, ergo
	# he has an alibi.)
	def counter(self,counter):
		ret = False
		if counter == self.suspect:
			ret = True
		if counter == self.weapon:
			ret = True
		if counter == self.room:
			ret = True
		return ret
		
	# Returns True if the accusation matches the casefile
	# False otherwise
	def checkCasefile(self,casefile):
		return casefile.checkAccusation(self.suspect,self.weapon,self.room)