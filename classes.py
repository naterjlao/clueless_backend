#!/usr/bin/python3
################################################################################
# File:            classes.py
# Subcomponent:    Clueless/Backend
# Language:        python3
# Author:          Nate Lao (nlao1@jh.edu)
# Date Created:    4/28/2020
# Description:
#			Contains the class definitions for the game.
#
################################################################################			
from globals import *

# A board is constructed of a 3x3 grid of rooms
# Every room is connected to room that is directly North, South, East or West of it.
# There are no diagonal connection between rooms.
# On a corner room, there is a secret passage that connects to the opposite
# corner room relative to the board. Therefore, there are only 4 rooms that have
# secret passages.
class Gameboard:
	def __init__(self,playerlist):
		# Observe that Rooms are captured, hallways must be accounted in
		# the player's location field
		self.rooms = []
		self.passageways = []
		self.playerlist = playerlist #include a reference to the game's PlayerList instance
		
		# Validate the given rooms
		if len(ROOMS) == 0:
			raise GameException("you cannot have a board game with no ROOMS")
		self.dimension = int(len(ROOMS) ** (1/float(2)))
		if self.dimension ** 2 != len(ROOMS):
			raise GameException("invalid number of rooms provided in ROOMS")
			
		# Add the rooms to the board
		for idx in range(0,len(ROOMS)):
			x_coordinate = int(idx % self.dimension)
			y_coordinate = int(idx / self.dimension)
			self.rooms.append(Room(ROOMS[idx],x_coordinate,y_coordinate))
			
		# TODO THIS is still fucked
		# Add the passageways to the board
		'''
		for idx in range(0,len(ROOM)):
			north = idx - self.dimension
			south = idx + self.dimension
			east  = idx + 1
			west  = idx - 1
			candidates = [north,south,east,west]

			# A room that 
			for elem in candidates:
		'''
		
	
	def __str__(self):
		ret = ""
		bufferspace = 0
		for name in (ROOMS + SUSPECTS):
			bufferspace = bufferspace if len(name) < bufferspace else len(name)
		
		# Visual output
		for x in range(0, self.dimension):
			for idx in range(0,(bufferspace*self.dimension)):
				ret += "-"
			ret += "\n"
			
			# Printout the room name
			room_row = []
			for y in range(0, self.dimension):
				room_row += self.getRooms()
				ret += "|"
				ret += room_row[y].name
				for idx in range(0,bufferspace - len(room_row[y].name)):
					ret += " "
			ret += "|"
			ret += "\n"

			# Printout the suspect names within the room
			for rowIdx in range(0,bufferspace):
				for y in range(0, self.dimension):
					rowIdx = room_row[y].getPlayers()
					ret += "|"
					if rowIdx < len(players):
						ret += players[rowIdx].suspect
						for idx in range(0,bufferspace - len(players[rowIdx].suspect)):
							ret += " "
					else:
						for idx in range(0,bufferspace):
							ret += " "
				ret += "|"
				ret += "\n"
		return ret
	
	# Returns a list of Player(s) at the specified location
	# Argument <position> is a string name
	# If there is one player, a singleton list is returned
	# If there is no player, an empty list is returned
	def getPlayer(self,position):
		ret = None
		# Search though rooms
		for room in self.rooms:
			if room.name == position:
				ret = room.getPlayer()
		
		if ret == None:
			# Search through passageways
			for passway in self.passageways:
				if room.name == room.getPlayer():
					ret = passway.getPlayer()
		return ret
	
	
	# Returns True iff the movement of choice is valid
	def validMove(self,playerId,choice):
		pass
	
	# Moves the player to the associated room of choice if possible
	def movePlayer(self,playerId,choice):
		pass

	# Returns the Room instance at a specified coordinate
	def getRoom(self,x_coordinate,y_coordinate):
		target = None
		# validate coordinate
		if (not (x_coordinate < self.dimension and y_coordinate < self.dimension)):
			raise GameException("invalid coordinates")
		for room in self.rooms:
			if (room.X == x_coordinate and room.Y == y_coordinate):
				target = room
		return target
		
	# Returns all Room instances on the board
	def getRooms(self):
		return self.rooms

	# Returns a dictionary representation the object as defined in-spec
	# TODO --- THIS IS NOT CONSISTENT WITH THE FK SPEC ---
	# Define it here:
	# {
	#	<location (either a room or passage way)> : <playerId or None>,
	#	...
	# }
	def getGameboard(self):
		pass
		'''
		ret = {}
		for player in playerlist.getPlayers():
			pId = player.getID()
			ret[pId] = 
		'''
		
class Room:
	def __init__(self,name,X,Y):
		self.name = name
		self.X = X
		self.Y = Y
		self.secretpassage = None # A Room
		self.passageways = []
		self.players = [] 	# list of Player instances that currently occupy the Room
							# MUST be consistent with Player location

	# Defines the name of the room
	def setName(self,name):
		self.name = name
		
	# Adds a connecting passageway
	def addPassageway(self,passageway):
		self.passageway.append(passageway)
		
	# A Secret Passage is basically a Room
	def addSecretPassage(self,room):
		self.secretpassage = room
		
	# A Room may be occupied by an unlimited amount of players
	def isOccupied(self):
		return False
	
	# Returns all potential movement choices based on this Room's position 
	def getChoices(self):
		return [] # TODO
	
	# Returns a list of all Players in the Room
	def getPlayers(self):
		return self.players
	
	# Returns True iff the requested choice name
	# is a valid movement in respect to the board
	# Observe that a passageway is the choice unless
	# the secret passage is a room. In the latter
	# case the choice would be a room string.
	def isValid(self,choiceName):
		return False # TODO

# Connects two adjacent rooms
class PassageWay:
	def __init__(self,roomA,roomB):
		self.roomA = roomA
		self.roomB = roomB
		self.name = None
		self.Name()
		self.player = None # Only one player can occupy a PassageWay
	
	# Defines a the name of the passageway.
	# This is a lazy approach, we sort the names
	# alphabetically and concat to this string:
	# "<room1>-<room2>"
	# Where room1 < room2
	# All combination of 1-1 room passageways
	# are unique
	def setName(self):
		ret = None
		room1 = self.roomA.getName()
		room2 = self.roomB.getName()
		if room1 < room2:
			ret = "%s-%s" % (room1,room2)
		else:
			ret = "%s-%s" % (room2,room1)
	
	# Returns True if a Player is occupying a Hallway
	# Only one Player can occupy a Hallway
	def isOccupied(self):
		return self.player != None
	
	# Returns a singleton list of the Player that
	# in the Hallway (really a misnomer)
	def getPlayers(self):
		return [self.player] if self.player != None else []
	
	# Removes the Player from the Hallway.
	# Returns the Player that was removed
	# If there was no Player, returns None
	def removePlayer(self):
		player = self.player
		self.player = None
		return player
	
	# Returns True iff the choice is accessible from this passageway
	def isValid(self,choice):
		return False
		# TODO


# Defines a Player object
class Player:
	# A player has an ID and an assocatied suspect character.
	# A player also holds a hand of cards, a checklist used
	# for identifying suspects and a message that would 
	# be displayed to the UI
	def __init__(self,playerId):
		self.playerId = playerId
		self.suspect = None
		self.location = "INITIAL"
		self.message = None
		self.cards = []
		self.checklist = []
		self.state = "IN_PLAY" # "WIN", "LOSE"
	
	def __str__(self):
		return "%s : $s" % (self.playerId, self.suspect)
		
	def getID(self):
		return self.playerId
		
	# Adds a card to the Player's hand
	# The number of cards given to player is dependent on the number of players
	# in the game. This is because the cards are equally dispersed once the
	# case file is created. The types of cards the player has does not matter.
	def addCard(self,card):
		logger.log("Adding %s card to %s's hand" %(card,self.playerId))
		self.cards.append(card)
		
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
		return False # TODO review the requirements for the game at the target state
		
	# Associates a suspect string name to this player
	# Note: we assume that the selection is good.
	# (ie. the player cannot select a suspect that is already choosen
	def selectSuspect(self,suspect):
		logger.log("Assigning %s to %s" % (suspect,self.playerId))
		self.suspect = suspect

# Wrapper for holding the list of Players registered in the game
# In addition, a list of characters that are available are stored
# in this class.
class PlayerList:
	def __init__(self):
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
		if getPlayer(playerId) == None:
			self.players.append(Player(playerId))
			ret = True
		else:
			logger.log("Cannot add %s, player already exists" % playerId)
		return ret
	
	def getPlayers(self):
		return self.players
	
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

	# Assigns the suspect to the player. If the suspect is already assigned
	# a GameException is thrown.
	def selectPlayerSuspect(self,playerId,suspect):
		player = self.getPlayer(playerId)
		# verify if the suspect has already been picked
		if suspect in self.availableCharacters:
			raise GameException("%s has already been picked" % suspect)
		elif suspect in SUSPECTS:
			player.selectSuspect(suspect) 				# Assign the player to the suspect
			self.availableCharacters.remove(suspect)	# Remove the suspect from the list of available characters
		else:
			raise GameException("%s is not a suspect name" % suspect)
	
# Defines a Card object
# A card may either be a:
# - suspect
# - room
# - weapon
class Card:
	def __init__(self,name):
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
	def __init__(self):
		self.cards = {}
		for card in CARDS:
			self.cards[card] = "UNASSIGNED"
	
	# From the given PlayerList object and CaseFile
	# The CardManager randomly chooses three cards from the
	# deck to place in the case file
	def assign(self,players : PlayerList):
		pass # TODO
		
# Defines the CaseFile object in the game.
# There shall only be one CaseFile per instance of a game.
# The values assigned during initialization MUST NOT BE CHANGED
# The CaseFile must contain 1 card from each type:
# - suspect
# - weapon
# - room
class CaseFile:
	def __init__(self,suspectCard,roomCard,weaponCard):
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

# Custom exception class
class GameException(Exception):
	def __init__(self,msg):
		self.msg = msg
	def __str__(self):
		return msg
		
		