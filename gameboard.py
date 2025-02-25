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
		for room in self.rooms:
			self.logger.log("Room generated: %s" % room)
		
		# Add the passageways to the board
		self.logger.log("Generating Passageways")
		for room in self.rooms:
			x_coordinate = room.getX()
			y_coordinate = room.getY()
			delta_range = [-1,0,1]
			for x_delta in delta_range:
				for y_delta in delta_range:
					if abs(x_delta) != abs(y_delta): # exclude corners and origin
						candidateRoom = self.getRoomByCoor(x_coordinate + x_delta, y_coordinate + y_delta)
						candidatePWay = None
						if candidateRoom != room and candidateRoom != None:
							candidatePWay = PassageWay(room,candidateRoom,self.logger)
						if (candidatePWay != None) and (candidatePWay not in self.passageways):
							self.logger.log("Adding passageway: %s" % candidatePWay)
							self.passageways.append(candidatePWay)
		for pway in self.passageways:
			self.logger.log("Passageway generated: %s" % pway)
			
		# Add the super secret passages
		for secret in SECRET_PASSAGES:
			destA, destB = secret
			destA = self.getRoom(destA)
			destB = self.getRoom(destB)
			self.logger.log("Adding secret passages %s <-> %s" % (destA, destB))
			destA.addSecretPassage(destB)
			destB.addSecretPassage(destA)
	
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
				ret += self.getRoomByCoor(x,y).name
				for idx in range(0,bufferspace - len(self.getRoomByCoor(x,y).name)):
					ret += " " # padding
			ret += "|"
			ret += "\n"

			# Printout the suspect names within the room
			for rowIdx in range(0,len(SUSPECTS)):
				for x in range(0, self.dimension):
					players = self.getRoomByCoor(x,y).getPlayers()
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
			for player in pway.getPlayers():
				ret += str(player)
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
		for player in playerlist.fakePlayers:
			self.initial.addPlayer(player)

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
	
	# Returns list of Location objects that the player can go to at the current position
	# If the player does not exist on the board, (not in Hallways, Passageways or Initial)
	# Then an empty list is returned
	# Note that the return is always an list of objects
	def getMoveOptions(self,player):
		ret = None
		current_loc = self.getPlayerLoc(player)
		# Find all possible locations the player can go
		# There is a special exception to players that are currently in their initial positions
		if current_loc == self.initial:
			ret = [self.determineInitPassageway(player)]	# Return the singleton list of one passageway
		elif current_loc != None:
			ret = current_loc.getChoices()
		else:
			ret = []										# This only occurs if the game has not started
		return ret
	
	# Should only be called when a player is at his intial position
	# We determine what passageway the player will go to as his
	# opening move
	def determineInitPassageway(self,player):
		idx = SUSPECTS.index(player.getSuspect())		# Reference the player's index position
		roomAidx, roomBidx = INITIAL[idx]				# Map the index tot he INITIAL tuple
		roomA = self.getRoom(ROOMS[roomAidx])			# Find the referenced rooms
		roomB = self.getRoom(ROOMS[roomBidx])
		passageway = self.getPassageway(roomA,roomB)
		return passageway
	
	# Returns True iff the movement is valid from one location to another
	# This is based on the state of succeeding location and the current player's state
	# There is an edge case for the initial starting position
	def validMove(self,player,start,dest):
		# Check if the player is not locked
		if player.state == PLAYER_LOCKED:
			raise GameException(player, "cannot move right now")
	
		if start == self.initial:
			return self.determineInitPassageway(player) == dest
		else:
			return dest in start.getChoices()
	
	# Moves the player to the associated room of choice if possible
	# The force parameter shall only be used if the player needs to
	# be moved because of a suggestion. If a suggestion is made to 
	# the player, the player must move to the room of the suggestion
	def movePlayer(self,player,choiceName,force=False):
		start = self.getPlayerLoc(player)
		dest = self.getLoc(choiceName)
	
		if force:
		
			# Move the player to the next location without validation
			self.logger.log("Forcefully moving %s from %s to %s" % (str(player),start.getName(),dest.getName()))
			start.removePlayer(player)
			dest.addPlayer(player)
		
		elif self.validMove(player,start,dest):
		
			# Move the player to the next location
			self.logger.log("Moving %s from %s to %s" % (str(player),start.getName(),dest.getName()))
			start.removePlayer(player)
			dest.addPlayer(player)
			
			# If the player had just moved to a room, he MUST make a suggestion
			if (dest.isRoom()):
				player.state = PLAYER_SUGGEST
				player.message = "MAKE A SUGGESTION! ...plz"
				
			# If the player had just moved into a hallway
			else:
				player.state = PLAYER_IN_PLAY
		else:
			GameException(player,"Invalid move")

	# Removes the player from the gameboard
	def removePlayer(self,player):
		pass

	# Returns Room or Passageway based on the name of the location
	def getLoc(self,name):
		target = None
		for loc in self.getAllPositions():
			if loc.getName() == name:
				target = loc
				break
		return target

	# Returns the room on the board that matches the given name
	def getRoom(self,name):
		target = None
		for room in self.rooms:
			if room.getName() == name:
				target = room
				break
		return target

	# Returns the Room instance at a specified coordinate
	# If the coordinates are invalid (ie. out of bounds), then None is returned
	def getRoomByCoor(self,x_coordinate,y_coordinate):
		target = None
		# validate coordinate
		if (not (x_coordinate < self.dimension and y_coordinate < self.dimension
				and x_coordinate >= 0 and y_coordinate >= 0)):
			self.logger.log("invalid coordinates given for Gameboard:getRoom()")
		for room in self.rooms:
			if (room.X == x_coordinate and room.Y == y_coordinate):
				target = room
		return target
	
	# Returns the associated passageway between the given room on the board
	def getPassageway(self,roomA,roomB):
		target = None
		for pway in self.passageways:
			if pway.isPassageWayFor(roomA,roomB):
				target = pway
				break
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

	def isRoom(self):
		return True
		
	def isPassageWay(self):
		return False

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
	
	# Returns only valid choices that the player can go to from this room
	def getChoices(self):
		self.logger.log("getting choices for %s" % self.getName())
		ret = []
		for pway in self.passageways:			# See if the passageway is valid
			if (not pway.isOccupied()):			# Add to the list of options
				ret.append(pway)
		if self.secretpassage != None:
			ret.append(self.secretpassage)		# Add the secret passage if possible
		return ret
	
	def addPlayer(self,player):
		self.logger.log("adding %s to %s" % (player,self.name))
		self.players.append(player)
	
	# Returns a list of all Players in the Room
	def getPlayers(self):
		return self.players
	
	# Returns true if the player is within the Room
	def hasPlayer(self,player):
		return player in self.players
		
	def removePlayer(self,player):
		self.players.remove(player) # TODO GameException verification

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
	
	def isRoom(self):
		return False
		
	def isPassageWay(self):
		return True
	
	def isPassageWayFor(self,roomA,roomB):
		ret = False
		if (self.roomA == roomA) and (self.roomB == roomB):
			ret = True
		elif (self.roomB == roomA) and (self.roomA == roomB):
			ret = True
		return ret
	
	# Returns all valid movement choices based on this Hallways's position
	# Note that the Player can go to any room, since they can be occupied by any
	# number of people
	def getChoices(self):
		self.logger.log("getting choices for %s" % self.getName())
		return [self.roomA, self.roomB]
	
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
	
	def addPlayer(self,player):
		self.player = player # TODO GameException verification
	
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
	def removePlayer(self,player):
		player = self.player
		self.player = None
		return player # TODO GameException validation
	