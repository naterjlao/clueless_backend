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
import random
from datetime import datetime
random.seed(datetime.now())	

# Defines a Card object
# A card may either be a:
# - suspect
# - room
# - weapon
class Card:
	def __init__(self,name,logger):
		self.logger = logger
		self.name = name
		self.owner = CARD_UNASSIGNED # Note this is assigned to a player or casefile object
	
	def __str__(self):
		return str(self.name)
		
	def getName(self):
		return self.name

	def assignTo(self,owner):
		if self.owner != CARD_UNASSIGNED:
			raise BackException("you cannot reassign cards in this game")
		else:
			self.owner = owner

	def getOwner(self):
		return self.owner

	def isUnassigned(self):
		return self.owner == CARD_UNASSIGNED

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
		self.casefile = None
		self.logger = logger
		self.cards = []
		self.generateCards()
	
	def __str__(self):
		ret = ""
		for card in self.cards:
			ret += str(card)
			ret += " - "
			ret += str(card.getOwner())
			ret += "\n"
		return ret
	
	# Returns a list of cards that are assigned to the player
	def getCards(self,player):
		playerCards = []
		for card in self.cards:
			if card.getOwner() == player:
				playerCards.append(card)
		return playerCards
	
	# Generates the deck of cards set to their initial values
	def generateCards(self):
		for name in CARDS:
			self.cards.append(Card(name,self.logger))
	
	# Picks out 3 random cards from the deck from each category
	# to load up the case file
	def loadCaseFile(self):
		candidate_suspect = None
		candidate_weapon = None
		candidate_room = None
		suspect_pool = []
		weapon_pool = []
		room_pool = []
		
		# Get the cards from each category
		for card in self.cards:
			if card.isSuspect():
				suspect_pool.append(card)
			if card.isWeapon():
				weapon_pool.append(card)
			if card.isRoom():
				room_pool.append(card)
		
		# TODO probably want to validate the randomness of this
		candidate_suspect = suspect_pool[random.randrange(len(suspect_pool))]
		candidate_weapon = weapon_pool[random.randrange(len(weapon_pool))]
		candidate_room = room_pool[random.randrange(len(room_pool))]
		
		if (candidate_suspect == None) or (candidate_weapon == None) or (candidate_room == None):
			raise BackException("could not load the case file... might be another issue")
		else:
			self.logger.log("loading up the case file with: %s, %s, %s" % (str(candidate_suspect),str(candidate_weapon),str(candidate_room)))
			self.casefile = CaseFile(candidate_suspect,candidate_weapon,candidate_room,self.logger)
			# Make sure to change the states of the cards that were loaded
			candidate_suspect.assignTo(self.casefile)
			candidate_weapon.assignTo(self.casefile)
			candidate_room.assignTo(self.casefile)
	
	# Returns all available cards that are not assigned
	def getAvailableCards(self):
		availCards = []
		for card in self.cards:
			if card.isUnassigned():
				availCards.append(card)
		return availCards
	
	# Information about who holds the cards are held in this datastructure
	def assign(self,playerlist):
		# This approach is similar to how we hand out cards in real life,
		# since this is only ran once when the game begins, I don't care
		# about the complexity of this algorithm
		availCards = self.getAvailableCards() # why doesn't python have do-while loops?
		players = playerlist.getPlayers()
		idx = 0 # players index
		while len(availCards) > 0:
			# Pick a random card from the available cards pool and assign it
			# a player in a round table fashion
			availCards[random.randrange(len(availCards))].assignTo(players[idx])
			
			idx = (idx + 1) % len(players) # wrap around
			availCards = self.getAvailableCards()
		
# Defines the CaseFile object in the game.
# There shall only be one CaseFile per instance of a game.
# The values assigned during initialization MUST NOT BE CHANGED
# The CaseFile must contain 1 card from each type:
# - suspect
# - weapon
# - room
class CaseFile:
	def __init__(self,suspectCard,weaponCard,roomCard,logger):
		self.logger = logger
		self.suspectCard = suspectCard
		self.weaponCard = weaponCard
		self.roomCard = roomCard

	def __str__(self):
		return "Case file"

	# Returns True if the accusation suspect, room and weapon
	# matches the values set in the case file.
	# False otherwise.
	def checkAccusation(self,suspect, weapon, room):
		ret = True
		if (self.suspectCard.name != suspect):
			ret = False
		if (self.weaponCard.name  != weapon):
			ret = False
		if (self.roomCard.name    != room):
			ret = False
		return ret
