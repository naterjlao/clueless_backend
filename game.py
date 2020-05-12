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
		self.cardmanager = CardManager(self.logger)
		self.state = STATE_INITIAL
		self.currentPlayer = None # NOTE the player Object, not the ID
		self.suggestion = None # this is the current suggestion object in play
		self.accusation = None # this is the current accusation object in play

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
	
	
	########################################################################
	# PUBLIC INTERFACE GLOBAL METHOD SENDERS
	# These methods must return a SINGLE dictionary
	# This dictionary will be sent to all players at the same signal cycle.
	########################################################################
	# Returns a Dictionary. The same dictionary is sent to ALL players
	def getGamestate(self):
		currentPlayer = self.playerlist.getCurrentPlayer()
		currentPlayerId = "No current player, game has not started" if currentPlayer == None else currentPlayer.getID()

		ret = {
				"currentPlayerId"     : currentPlayerId,
				"turnStatus"          : self.state,
				"availableCharacters" : self.playerlist.getAvailableCharacters(),
				"characters_in_game"  : self.playerlist.getCharactersInGame(),
				"game_has_begun"      : (self.state != STATE_INITIAL)
			}
			
		# Revert state back to MOVE (unless a suggestion action is called)
		# self.state = STATE_MOVE
		
		return ret
	
	# Returns a Dictionary. The same dictionary is sent to ALL players
	def getGameboard(self):
		return self.gameboard.getGameboard()

	# When a game exception is thrown, do not crash, instead alert the current
	# user that the choice is invalid
	def handleGameException(self,gexc):
		if DEBUG:
			print(gexc.msg)
		# Update the message attribute to all players, or the player that
		# sent the message
		if gexc.player == "all":
			for player in self.playerlist.getPlayers():
				player.updateMessage(gexc.msg)
		else:
			gexc.player.updateMessage(gexc.msg)
	
	
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
			# Don't allow the player to move if they need to suggest
			if player.state != PLAYER_SUGGEST:
				moveOptions = self.gameboard.getMoveOptions(player)
				moveOptStr = []
				for option in moveOptions:
					moveOptStr.append(option.getName())
				data.append({PLAYER_ID:player.playerId,DIRTY:True,PAYLOAD:moveOptStr})
		return data

	# Returns a list of Dictionaries that are sent to each player
	def getSuggestionOptions(self):
		# If a player is at a room, he can make a suggestion
		data = []
		if (self.state != STATE_INITIAL):
			allPlayers = self.playerlist.getPlayers()
			for player in allPlayers:
				self.logger.log("getting suggestions options for %s" % player)
				# A player can only suggest, if he can suggest
				if (player.state == PLAYER_SUGGEST):
					#accusePlayerOptions = []
					accuseOptions = []
					# under the fifth amendment, you are protected against self-incrimination
					for s in SUSPECTS:
						if (player.getSuspect() != s):
							accuseOptions.append(s)
					
					'''
					for p in allPlayers:
						if (p != player):
							accusePlayerOptions.append(p)
					# get the suspect names, not player id
					accuseOptions = list(map(lambda p : p.getSuspect(), accusePlayerOptions))
					'''
					# get all weapons
					weaponOptions = WEAPONS
					
					# only get the room the player is currently at
					if self.gameboard.getPlayerLoc(player).isPassageWay():
						raise BackException("you cannot suggest in a passageway")
					roomOptions = [self.gameboard.getPlayerLoc(player).getName()]
					payload = {"suspects":accuseOptions,"weapons":weaponOptions,"rooms":roomOptions}
					data.append({PLAYER_ID:player.playerId,DIRTY:True,PAYLOAD:payload})
		return data
		
	# Returns a list of Dictionaries that are sent to each player
	def getAccusationOptions(self):
		# If a player is at a room, he can make a suggestion
		data = []
		if (self.state != STATE_INITIAL):
			allPlayers = self.playerlist.getPlayers()
			for player in allPlayers:
				self.logger.log("getting accusation options for %s" % player)
				# A player can accuse at anytime
				#accusePlayerOptions = []
				accuseOptions = []
				# under the fifth amendment, you are protected against self-incrimination
				for s in SUSPECTS:
					if (player.getSuspect() != s):
						accuseOptions.append(s)
				'''
				for p in allPlayers:
					if (p != player):
						accusePlayerOptions.append(p)
				# get the suspect names, not player id
				accuseOptions = list(map(lambda p : p.getSuspect(), accusePlayerOptions))
				'''
				# get all weapons
				weaponOptions = WEAPONS
				
				# get all rooms
				roomOptions = ROOMS
				
				payload = {"suspects":accuseOptions,"weapons":weaponOptions,"rooms":roomOptions}
				data.append({PLAYER_ID:player.playerId,DIRTY:True,PAYLOAD:payload})
		return data
		
	# Returns a list of Dictionaries that are sent to each player
	def getChecklists(self):
		data = []
		for player in self.playerlist.getPlayers():
			checklist = player.getChecklist()
			data.append({PLAYER_ID:player.getID(),DIRTY:True,PAYLOAD:checklist})
		return data
		
	# Returns a list of Dictionaries that are sent to each player
	def getCardlists(self):
		data = []
		for player in self.playerlist.getPlayers():
			# I heard you like one-liners (converts the card object into their string representation)
			cards = list(map(lambda c: str(c), self.cardmanager.getCards(player)))
			data.append({PLAYER_ID:player.getID(),DIRTY:True,PAYLOAD:{"cardList":cards}})
		return data
		
	# Returns a list of Dictionaries that are sent to each player
	def getMessages(self):
		data = []
		for player in self.playerlist.getPlayers():
			message,color = player.getMessage()
			data.append({PLAYER_ID:player.getID(),DIRTY:True,PAYLOAD:{"message":message,"color":color}})
		self.playerlist.resetMessages()
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
		try:
			# Validate if all players are ready to play
			self.playerlist.validatePlayers()
		
			# Remove all suspects from the available characters list
			self.playerlist.lockAvailableCharacters()
			
			# Load up the case file
			self.cardmanager.loadCaseFile()

			# Assign out the cards to the players
			self.cardmanager.assign(self.playerlist)
			
			# Once the cards are assigned, we check off the checklists for all players
			for player in self.playerlist.getPlayers():
				cards = self.cardmanager.getCards(player)
				for card in cards:
					player.updateChecklist(card.getName())

			# Assign the starting positions of all the players
			self.gameboard.intializePlayers(self.playerlist)
			
			# Set the starting player
			self.playerlist.startGame()
		
			# Set the game state to STARTED
			self.state = STATE_STARTED
			
		except GameException as gexc:
			self.handleGameException(gexc)
		
		
	def selectMove(self,playerId,choice):
		try:
			player = self.playerlist.getPlayer(playerId)
			# Must validate that it is the current player's turn
			if self.playerlist.hasTurn(player) and player.state != PLAYER_LOSE and player.state != PLAYER_LOCKED:
				self.gameboard.movePlayer(player,choice)
				# If the player has just moved to a room, he must make a suggestion
				# Else, the turn counter is incremented
				if (player.state != PLAYER_SUGGEST):
					self.playerlist.nextCurrentPlayer()
			else:
				raise GameException(player,"Cannot move, it is not your turn")
		except GameException as gexc:
			self.handleGameException(gexc)
		
	def selectCard(self,playerId,choice):
		pass # NOT USED
		
	def passTurn(self,playerId):
		try:
			currentPlayer = self.playerlist.getCurrentPlayer()
			# A pass turn signal must be 
			# - triggered by the current player,
			# - the current player must not be forced to make a suggestion
			# - the current player must not be in a state of defense
			if (currentPlayer != None) and (currentPlayer.getID() == playerId) \
				and (currentPlayer.state != PLAYER_SUGGEST) \
				and (currentPlayer.state != PLAYER_DEFEND):
				self.playerlist.nextCurrentPlayer()
				
				newCurrentPlayer = self.playerlist.getCurrentPlayer()
				moveOptions = self.gameboard.getMoveOptions(newCurrentPlayer)
				if len(moveOptions) > 0:
					newCurrentPlayer.state = PLAYER_MOVE
				else :
					newCurrentPlayer.state = PLAYER_IN_PLAY # player might be able to suggest, but can't move anywhere
					
			else:
				raise GameException(currentPlayer,"cannot pass turn")
		except GameException as gexc:
			self.handleGameException(gexc)
	
	# Enables the game's suggestion state
	def startSuggestion(self,playerId):
		self.state = STATE_SUGGESTION
	
	# The player suggests an accused player
	def proposeSuggestion(self,playerId,suspect,weapon):
		try:
			# Get the location of the current player, since that
			# is what will be used in a suggestion
			currentPlayer = self.playerlist.getPlayer(playerId)
			room = self.gameboard.getPlayerLoc(currentPlayer).getName()
			
			# Store a suggestion object in memory
			self.suggestion = Suggestion(currentPlayer,suspect,weapon,room,self.logger)
			
			# Do the actions associated with a suggestion
			self.playerlist.makeSuggestion(self.suggestion,self.gameboard)
		except GameException as gexc:
			self.handleGameException(gexc)
	
	# NOTE Argument type is redundant, card can be derived by the gamestate because that is trivial	
	def disproveSuggestion(self,playerId,card,type,cannotDisprove):
		try:
			targetPlayer = self.playerlist.getPlayer(playerId)
			
			# Perform the action about the suggestion
			self.playerlist.endSuggestion(targetPlayer,card,self.suggestion,self.gameboard,self.cardmanager.casefile,cannotDisprove)
			
			# Blow away the suggestion instance
			self.suggestion = None
			
			# Revert game state to normal
			self.state = STATE_STARTED
		except GameException as gexc:
			self.handleGameException(gexc)

	# Enables the game accusation state
	def startAccusation(self,playerId):
		self.state = STATE_ACCUSATION
	
	def proposeAccusation(self,playerId,accusedId,weapon,room):
		try:
			accuser = self.playerlist.getPlayer(playerId)
			suspect = self.playerlist.getPlayer(accusedId)
		
			# The player calls an accusation and an accusation object is built
			self.accusation = Accusation(accuser,suspect.getSuspect(),weapon,room)
			
			# Validate against the casefile
			isCorrect = self.accusation.checkCaseFile()
			
			# Throw the game into a state of accusation
			# (this is currently pointless, because evaluation comes immediately after)
			self.state = STATE_ACCUSATION
			
			# If the accusation is true, the game ends
			# - the accuser is made the winner
			# - the suspect loses
			if (isCorrect):
				accuser.state = PLAYER_WIN
				suspect.state = PLAYER_LOSE
				# The game ends
				self.state = STATE_END
			
			# If the accusation is false, the game resumes
			# - the accuser loses the game, and may not proceed
			else:
				accuser.state = PLAYER_LOSE
				# The game is thrown back to normal
				self.state = STATE_STARTED
		
			# Blow away the accusation object
			self.accusation = None
		except GameException as gexc:
			self.handleGameException(gexc)
	
	# NOTE this is not used, validation immediately comes from the case file
	def disproveAccusation(self,playerId,card,type,cannotDisprove):
		pass
		
	# Gracefully remove the player from the game
	def removePlayer(self,playerId):
		target = self.playerlist.removePlayer(playerId)
		self.gameboard.removePlayer(target)

