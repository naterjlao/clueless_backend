#!/usr/bin/python3
################################################################################
# File:            gameboard.py
# Subcomponent:    Clueless/Backend
# Language:        python3
# Author:          Nate Lao (nlao1@jh.edu)
# Date Created:    5/1/2020
# Description:
#			Contains the gameboard related class declarations for Clueless.
#
################################################################################

from utils import *
from globals import *

# A board is constructed of a 3x3 grid of rooms
# Every room is connected to room that is directly North, South, East or West of it.
# There are no diagonal connection between rooms.
# On a corner room, there is a secret passage that connects to the opposite
# corner room relative to the board. Therefore, there are only 4 rooms that have
# secret passages.
class Gameboard:
	def __init__(self,logger):
		self.logger = logger
		# Observe that Rooms are captured, hallways must be accounted in
		# the player's location field
		self.rooms = []
		self.passageways = []
		self.initial = Room("INITIAL",-1,-1,self.logger) # Singleton initial player starting space
		
		# Validate the given rooms
		if len(ROOMS) == 0:
			raise BackendException("you cannot have a board game with no ROOMS")
		self.dimension = int(len(ROOMS) ** (1/float(2)))
		if self.dimension ** 2 != len(ROOMS):
			raise BackendException("invalid number of rooms provided in ROOMS")
		
		# Add the rooms to the board
		self.logger.log("Generating Rooms")
		for idx in range(0,len(ROOMS)):
			x_coordinate = int(idx % self.dimension)
			y_coordinate = int(idx / self.dimension)
			self.rooms.append(Room(ROOMS[idx],x_coordinate,y_coordinate,self.logger))
		self.logger.log("Rooms generated: %s" % self.rooms)
		
		# Add the passageways to the board
		self.logger.log("Generating Passageways")
		for room in self.rooms:
			x_coordinate = room.getX()
			y_coordinate = room.getY()
			delta_range = [-1,0,1]
			for x_delta in delta_range:
				for y_delta in delta_range:
					if abs(x_delta) != abs(y_delta): # exclude corners and origin
						candidateRoom = self.getRoom(x_coordinate + x_delta, y_coordinate + y_delta)
						candidatePWay = None
						if candidateRoom != room and candidateRoom != None:
							candidatePWay = PassageWay(room,candidateRoom,self.logger)
						if (candidatePWay != None) and (candidatePWay not in self.passageways):
							self.logger.log("Adding passageway: %s" % candidatePWay)
							self.passageways.append(candidatePWay)
		self.logger.log("Passageways generated: %s" % self.passageways)
	
	def __str__(self):
		ret = ""
		bufferspace = 0
		for name in (ROOMS + SUSPECTS):
			bufferspace = bufferspace if len(name) < bufferspace else len(name)
		
		# Visual output of the Board Rooms
		for y in range(0, self.dimension):
			for idx in range(0,(bufferspace*self.dimension) + self.dimension + 1):
				ret += "-" # printout ----- border
			ret += "\n"
			
			# Printout the room name
			for x in range(0, self.dimension):
				ret += "|"
				ret += self.getRoom(x,y).name
				for idx in range(0,bufferspace - len(self.getRoom(x,y).name)):
					ret += " " # padding
			ret += "|"
			ret += "\n"

			# Printout the suspect names within the room
			for rowIdx in range(0,len(SUSPECTS)):
				for x in range(0, self.dimension):
					rowIdx = 0
					players = self.getRoom(x,y).getPlayers()
					ret += "|"
					if rowIdx < len(players):
						ret += players[rowIdx].suspect
						for idx in range(0,bufferspace - len(players[rowIdx].suspect)):
							ret += " " # name row
					else:
						for idx in range(0,bufferspace):
							ret += " " # empty row
				ret += "|"
				ret += "\n"
		
		for idx in range(0,(bufferspace*self.dimension) + self.dimension + 1):
			ret += "-" # printout ----- border
		ret += "\n"
		
		# Printout the Passageways
		for pway in self.passageways:
			ret += str(pway) + " "
			ret += "(%s, %s)" % (pway.roomA, pway.roomB)
			ret += ": "
			ret += str(pway.getPlayers())
			ret += "\n"

		for idx in range(0,(bufferspace*self.dimension) + self.dimension + 1):
			ret += "-" # printout ----- border
		ret += "\n"
		
		return ret
	
	# Returns a list of all Rooms and Passageways
	def getAllPositions(self):
		return (self.rooms + self.passageways + [self.initial])
	
	# Initializes players to their starting positions
	def intializePlayers(self,playerlist):
		for player in playerlist.getPlayers():
			self.initial.addPlayer(player)
			
	''' CANDIDATE FOR DEPRECATION
	# Returns a list of dictionaries containing the following information
	# - playerId: string of the playerId at a room
	# - location: location of the player
	def getGameboard(self):
		ret = []
		for loc in self.getAllPositions():
			for player in loc.getPlayers():
				ret.append({PLAYER_ID:player.getID(),LOCATION:loc.getName()})
		return ret
	'''
	# Returns a dictionary.
	# Contains keys that are named after every possible location on the board include INITIAL
	# The value of each key maps to list of SUSPECTS that occupy the location
	# If no suspect occupies a location, an empty [] is returned
	def getGameboard(self):
		ret = {}
		for position in self.getAllPositions():
			players = position.getPlayers()
			suspects = []
			for player in players:
				suspects.append(player.getSuspect())
			ret[position.getName()] = suspects
	
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
	
	# Returns the Room or PassageWay of the player,
	# If the player does not exist in the board (neither Hallway, PassageWay or Initial),
	# then None is returned
	def getPlayerLoc(self,player):
		ret = None
		for position in self.getAllPositions():
			if position.hasPlayer(player):
				ret = position
				break # this might cause issues down the line
		return ret
	
	# Returns list of room string names that the player can go to at the current position
	# If the player does not exist on the board, (not in Hallways, Passageways or Initial)
	# Then an empty list is returned
	def getMoveOptions(self,player):
		ret = None
		current_loc = self.getPlayerLoc(player)
		# Find all possible locations the player can go
		# There is a special exception to players that are currently in their initial positions
		if current_loc == self.initial:
			ret = [] # TODO 
		elif current_loc != None:
			ret = current_loc.getChoices()
		else:
			ret = []
		# Sanity check
		if ret == None:
			raise GameError("could not return a list of options, not even empty list")
		return ret
			
	# Returns True iff the movement is valid
	# This is based on the state of succeeding location and the current player's state
	def validMove(self,player,choice):
		pass
	
	# Moves the player to the associated room of choice if possible
	def movePlayer(self,player,choice):
		pass

	# Removes the player from the gameboard
	def removePlayer(self,player):
		pass

	# Returns the Room instance at a specified coordinate
	# If the coordinates are invalid (ie. out of bounds), then None is returned
	def getRoom(self,x_coordinate,y_coordinate):
		target = None
		# validate coordinate
		if (not (x_coordinate < self.dimension and y_coordinate < self.dimension
				and x_coordinate >= 0 and y_coordinate >= 0)):
			self.logger.log("invalid coordinates given for Gameboard:getRoom()")
		for room in self.rooms:
			if (room.X == x_coordinate and room.Y == y_coordinate):
				target = room
		return target
		
	# Returns all Room instances on the board
	def getRooms(self):
		return self.rooms
		
class Room:
	def __init__(self,name,X,Y,logger):
		self.logger = logger
		self.name = name
		self.X = X
		self.Y = Y
		self.secretpassage = None # A Room, so far, there can only be one secret passage per room
		self.passageways = []
		self.players = [] 	# list of Player instances that currently occupy the Room
							# MUST be consistent with Player location
							
	def __str__(self):
		return self.name

	# Room coordinates
	def getX(self):
		return self.X
	def getY(self):
		return self.Y

	# Defines the name of the room
	def setName(self,name):
		self.name = name
		
	def getName(self):
		return self.name
		
	# Adds a connecting passageway
	def addPassageway(self,passageway):
		if passageway not in self.passageways:
			self.logger.log("Adding passageway %s to room %s" % (passageway, self.name))
			self.passageways.append(passageway)
		else:
			self.logger.log("Could not add passageway %s to room %s" % (passageway, self.name))
		
	# A Secret Passage is basically a Room
	def addSecretPassage(self,room):
		self.secretpassage = room
		
	# A Room may be occupied by an unlimited amount of players
	def isOccupied(self):
		return False
	
	# Returns all potential movement choices based on this Room's position 
	def getChoices(self):
		return [] # TODO
	
	def addPlayer(self,player):
		self.logger.log("adding %s to %s" % (player,self.name))
		self.players.append(player)
	
	# Returns a list of all Players in the Room
	def getPlayers(self):
		return self.players
	
	# Returns true if the player is within the Room
	def hasPlayer(self,player):
		return player in self.players

# Connects two adjacent rooms
class PassageWay:
	def __init__(self,roomA,roomB,logger):
		self.logger = logger
		self.roomA = roomA
		self.roomB = roomB
		self.name = self.setName()
		self.player = None # Only one player can occupy a PassageWay
		# Once a passage way in generated, it needs to associate the rooms with it
		self.roomA.addPassageway(self)
		self.roomB.addPassageway(self)
	
	def __str__(self):
		return self.name
	
	# Passageways are bi-directional
	def __eq__(self,other):
		ret = True
		if self.__class__ != other.__class__:
			ret = False
		elif self.name != other.name:
			ret = False
		return ret
	
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
		return ret
	
	def getName(self):
		return self.name
	
	# Returns True if a Player is occupying a Hallway
	# Only one Player can occupy a Hallway
	def isOccupied(self):
		return self.player != None
	
	# Returns a singleton list of the Player that are
	# in the Hallway (really a misnomer)
	def getPlayers(self):
		return [self.player] if self.player != None else []
		
	# Returns true if the player is within the Hallway
	def hasPlayer(self,player):
		return player == self.player
	
	# Removes the Player from the Hallway.
	# Returns the Player that was removed
	# If there was no Player, returns None
	def removePlayer(self):
		player = self.player
		self.player = None
		return player
	