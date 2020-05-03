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
from utils import *
from globals import *
from gameboard import *
from players import *
from cards import *

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
		self.state = STATE_INITIAL
		self.currentPlayer = None # NOTE the player Object, not the ID
		self.suggestionCharacter = None

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
	
	# Game
	
	
	########################################################################
	# PUBLIC INTERFACE GLOBAL METHOD SENDERS
	# These methods must return a SINGLE dictionary
	# This dictionary will be sent to all players at the same signal cycle.
	########################################################################
	# Returns a Dictionary. The same dictionary is sent to ALL players
	def getGamestate(self):
		''' CANDIDATE FOR DEPRECATION
		if (self.state == STATE_INITIAL):
			playerId = "No current player, game has not started"
		else:
			playerId = self.currentPlayer.getID()
		'''
		currentPlayer = self.playerlist.getCurrentPlayer()
		currentPlayerId = "No current player, game has not started" if currentPlayer == None else currentPlayer.getID()

		ret = {
				"currentPlayerId"     : currentPlayerId,
				"turnStatus"          : self.state,
				"availableCharacters" : self.playerlist.getAvailableCharacters(),
				"game_has_begun"      : (self.state != STATE_INITIAL)
			}
		return ret
	
	# Returns a Dictionary. The same dictionary is sent to ALL players
	def getGameboard(self):
		return self.gameboard.getGameboard()

	# When a game exception is thrown, do not crash, instead alert the current
	# user that the choice is invalid
	def handleGameException(self,gexc):
		pass # so far, do nothing.
	
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
	def getPlayerstates(self):
		# Data preprocessing is needed
		data = []
		for elem in self.playerlist.getPlayerstates():
			data.append({PLAYER_ID:elem[PLAYER_ID],DIRTY:True,PAYLOAD:elem})
		return data
		
	# Returns a list of Dictionaries that are sent to each player
	def getMoveOptions(self):
		# Data preprocessing is needed
		data = []
		for player in self.playerlist.getPlayers():
			moveOptions = self.gameboard.getMoveOptions(player)
			moveOptStr = []
			for option in moveOptions:
				moveOptStr.append(option.getName())
			data.append({PLAYER_ID:player.playerId,DIRTY:True,PAYLOAD:moveOptStr})
		return data

	# Returns a list of Dictionaries that are sent to each player
	def getSuggestionOptions(self):
		return [] # TODO
		
	# Returns a list of Dictionaries that are sent to each player
	def getAccusationOptions(self):
		return [] # TODO
		
	# Returns a list of Dictionaries that are sent to each player
	def getChecklists(self):
		return [] # TODO
		
	# Returns a list of Dictionaries that are sent to each player
	def getCardlists(self):
		return [] # TODO
		
	# Returns a list of Dictionaries that are sent to each player
	def getMessages(self):
		data = []
		for player in self.playerlist.getPlayers():
			message,color = player.getMessage()
			data.append({PLAYER_ID:player.getID(),DIRTY:True,PAYLOAD:{"message":message,"color":color}})
		return data

	########################################################################
	# PUBLIC INTERFACE METHODS PROCESSORS
	########################################################################
	def addPlayer(self,playerId):
		try:
			self.playerlist.addPlayer(playerId)
		except GameException as gexc:
			self.handleGameException(gexc)
		
	def selectSuspect(self,playerId,suspect):
		try:
			self.playerlist.selectPlayerSuspect(playerId,suspect)
		except GameException as gexc:
			self.handleGameException(gexc)

	# Useless signal, does not matter
	# TODO actually, this might be a lie, we could use this as the trigger for addPlayer
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
		# Remove all suspects from the available characters list
		# Assign out the cards to the players
		# Generate the case file with a random selection of cards
		# Assign the starting positions of all the players
		self.gameboard.intializePlayers(self.playerlist)
		
		# Set the starting player
		self.playerlist.startGame()
	
		# Set the game state to STARTED
		self.state = STATE_STARTED
		
	def selectMove(self,playerId,choice):
		try:
			player = self.playerlist.getPlayer(playerId)
			# Must validate that it is the current player's turn
			if self.playerlist.hasTurn(player):
				self.gameboard.movePlayer(player,choice)
			else:
				raise GameException(player,"Cannot move, it is not your turn")
		except GameException as gexc:
			self.handleGameException(gexc)
		
	def selectCard(self,playerId,choice):
		pass
	
	def passTurn(self,playerId):
		currentPlayer = self.playerlist.getCurrentPlayer()
		# A pass turn signal can only be triggered by the current player
		if (currentPlayer != None) and (currentPlayer.getID() == playerId):
			self.playerlist.nextCurrentPlayer()
		else:
			pass # TODO send a message to all other players that you cannot pass turn at this state
		
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
	def removePlayer(self,playerId):
		target = self.playerlist.removePlayer(playerId)
		self.gameboard.removePlayer(target)

