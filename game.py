#!/usr/bin/python3
################################################################################
# File:            game.py
# Subcomponent:    Clueless/Backend
# Language:        python3
# Author:          Nate Lao (nlao1@jh.edu)
# Date Created:    4/28/2020
# Description:
#			Defines the main game instance object to be held in Memory when
#			the server starts up. Defined below are the interface methods
#			for the Serverside subsystem component for the Clueless server.
#			This is a represenation of ONE game instance. In theory, another
#			Game instance thread can run concurrent and without collision
#			with multithreading.
################################################################################

# Import classes
from classes import *
from globals import *

# Defines the Game object, the primary interface to the game instance
class Game:

	# Generates the game object.
	# This must be intialized before any requests or signals are in process
	def __init__(self):
		# Create the logger object per game instance, shared amongst all children objects
		self.logger = Logger()
	
		self.playerlist = PlayerList(self.logger)
		self.gameboard = Gameboard(self.logger)
		self.cardManager = CardManager(self.logger)
		self.turnStatus = "INITIAL"
		
		# Signal gamestate fields
		self.currentPlayer = None # NOTE the player Object, not the ID
		self.state = None # "INITIAL", "STARTED", "SUGGESTION", "ACCUSATION", "END" # might want to change so that they don't complain
		self.suggestionCharacter = None
		self.availableCharacters = None

	# Debugger printout
	def __str__(self):
		ret = ""
		ret+= "GAMEBOARD"                + "\n"
		ret+= str(self.gameboard)        + "\n"
		ret+= "------------------------" + "\n"
		ret+= "PLAYER LIST"              + "\n"
		ret+= str(self.playerlist)       + "\n"
		ret+= "------------------------"
		return ret
		
	########################################################################
	# AUXILIARY METHODS
	########################################################################
		
	
	
	# Updates the turn of the player at the given moment.
	def updateTurnStatus(self):
		self.turnStatus = self.gameboard.updateTurnStatus()
		
	# Updates the games availableCharacters instance
	# Must be called every time a character is allocated to a player
	def updateAvailableCharacters(self):
		self.availableCharacters = self.playerlist.getAvailableCharacters()
		
	########################################################################
	# PUBLIC INTERFACE GLOBAL METHOD SENDERS
	# These methods must return a SINGLE dictionary
	# This dictionary will be sent to all players at the same signal cycle.
	########################################################################
	# Returns a Dictionary. The same dictionary is sent to ALL players
	def getGamestate(self):
		ret = {
				"currentPlayerId"    : self.currentPlayer.getID(),
				"turnStatus"         : self.state,
				"availableChracters" : self.availableCharacters
			}
		return ret
		
	########################################################################
	# PUBLIC INTERFACE TARGETED METHOD SENDERS
	# These methods must return a LIST containing dictonaries.
	# Each dictionary must have:
	# - playerId : the intended reciever of the message
	# - dirty    : True if the message has been updated between cycles
	# - payload  : a dictionary containing the essential information that
	#              target will need.
	########################################################################
	# Returns a list of Dictionaries that are sent to each player
	def getGameboard(self):
		# Data preprocessing is needed
		data = []
		for elem in self.gameboard.getGameboard():
			# The payload really only needs to contain the location
			# since each signal is targeted to each individual player
			payload = {LOCATION:elem[LOCATION]}
			data.append({PLAYER_ID:elem[PLAYER_ID],DIRTY:True,PAYLOAD:payload})
		return data
	
	# Returns a list of Dictionaries that are sent to each player
	def getPlayerstates(self):
		# Data preprocessing is needed
		data = []
		for elem in self.playerlist.getPlayerstates():
			data.append({PLAYER_ID:elem[PLAYER_ID],DIRTY:True,PAYLOAD:elem})
		return data
		
	# Returns a list of Dictionaries that are sent to each player
	def getMoveOptions(self):
		data = []
		for player in self.playerlist.getPlayers():
			moveOptions = self.gameboard.getMoveOptions(player)
			data.append({PLAYER_ID:player.playerId,DIRTY:True,PAYLOAD:moveOptions})
		return data

	# Returns a list of Dictionaries that are sent to each player
	def getSuggestionOptions(self):
		pass
		
	# Returns a list of Dictionaries that are sent to each player
	def getAccusationOptions(self):
		pass
		
	# Returns a list of Dictionaries that are sent to each player
	def getChecklists(self):
		pass
		
	# Returns a list of Dictionaries that are sent to each player
	def getMessages(self):
		pass

	########################################################################
	# PUBLIC INTERFACE METHODS PROCESSORS
	########################################################################
	def addPlayer(self,playerId):
		#try:
		self.playerlist.addPlayer(playerId)
		#except GameException as gexc:
		#	print(gexc) # TODO -- push message to player's message board
		
	def selectSuspect(self,playerId,suspect):
		#try:
		self.playerlist.selectPlayerSuspect(playerId,suspect)
		self.updateAvailableCharacters()
		#except GameException as gexc:
		#	print(gexc) # TODO -- push message to player's message board

	# Useless signal, does not matter
	def enteredGame(self,playerId):
		pass
	
	# Sets up the CaseFile and assigns the cards out to the players.
	# Sets the game state to STARTED
	# Assigns players to their intial positions
	# It is assumed that:
	# - players have been assigned to suspects
	# - no other players will join
	# - the CardManager is properly initialized
	def startGame(self):
		# TODO
		# Remove all suspects from the available character list
		# Assign out the cards to the players
		# Generate the case file with a random selection of cards
		# Assign the starting positions of all the players
		self.gameboard.intializePlayers(self.playerlist)
		
		# Set the starting player
		self.currentPlayerId = self.playerlist.getPlayerBySuspect(SUSPECTS[0])
		self.state = "STARTED"
		
	def selectMove(self,playerId,choice):
		pass
		
	def selectCard(self,playerId,choice):
		pass
	
	def passTurn(self,playerId,choice):
		pass
		
	def startSuggestion(self,playerId):
		pass
	def proposeSuggestion(self,playerId,accussedId,weapon):
		pass
	def dispoveSuggestion(self,playerId,card,type,cannotDisprove):
		pass # NOTE Argument type is redundant, card can be derived by the gamestate because that trivial

	def startAccusation(self,playerId):
		pass
	def proposeAccusation(self,playerId,accussedId,weapon,room):
		pass # NOTE The options for an accusation is not constrained
	def disproveAccusation(self,playerId,card,type,cannotDisprove):
		pass # NOTE Argument <type> is redundant, card can be derived by the game itself because this is stupidly trivial
		
	# Gracefully remove the player from the game
	def removePlayer(self):
		pass







































		