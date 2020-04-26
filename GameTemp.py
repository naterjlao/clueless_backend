
# THIS IS A DEMO, REMOVE THIS

class Game:
	def __init__(self):
		self.gamestate = {"started":False}
		self.gameboard = Gameboard()
		self.players = PlayerList()
		
		# Pass in a reference to the gameboard
		# The gameboard lives as part of
		# the game, but not a part of the player list
		# The player list must be able to access it
		# somehow, so we pass a reference to it.
		self.players.setGameboard(self.gameboard) 	

	# DEBUG METHODS
	def __str__(self):
		returnStr = str(self.gameboard) + "\n" 
		returnStr+= str(self.players) + "\n"
		returnStr+= "Gamestate: "
		for k in self.gamestate:
			returnStr += k + "=" + str(self.gamestate[k]) + ", "
		return returnStr

	# PUBLIC SENDER METHODS
	
	# Returns a dict
	def getGamestate(self):
		return self.gamestate
		
	# Returns a dict
	def getGameboard(self):
		return self.gameboard.toDict()
	
	# Returns a list of dicts
	def getPlayerstates(self):
		return self.players.getPlayerstates()
		
	# Returns a list of dicts
	def getChecklists(self):
		pass # NOTE not handled in demo
		
	# Returns a list of dicts
	def getMoveOptions(self):
		return self.players.getMoveOptions()
	
	# Returns a list of dicts
	def getCardLists(self):
		return self.players.getCardLists()

	# Returns a list of dicts
	def getMessages(self):
		return self.players.getMessages()
	
	# PUBLIC RECIEVER METHODS
	def startGame(self):
		self.gamestate["started"] = True
	
	def selectMove(self,playerId,choice):
		self.players.movePlayer(playerId,choice)
	
	def selectCard(self,playerId,choice):
		pass # NOTE not handled in demo
	
	def addPlayer(self,playerId):
		self.players.addPlayer(playerId);

# Represents the position of every player relative to the board
class Gameboard:
	def __init__(self):
		self.spaces = {"NW":None,"NE":None,"SE":None,"SW":None}
	
	def __str__(self):
		returnStr = ""
		returnStr+= " " if self.spaces["NW"] == None else str(self.spaces["NW"])
		returnStr+= "|"
		returnStr+= " " if self.spaces["NE"] == None else str(self.spaces["NE"])
		returnStr+= "\n"
		returnStr+= " " if self.spaces["SW"] == None else str(self.spaces["SW"])
		returnStr+= "|"
		returnStr+= " " if self.spaces["SE"] == None else str(self.spaces["SE"])
		return returnStr
	
	# Validates the requested move
	def validMove(self,player,move):
		valid = True
		# False if another something already occupies that space
		if self.spaces[move] != None:
			valid = False
		# False if the player cannot physically move to the space
		if player.location == "NW" and move == "SE":
			valid = False
		if player.location == "SE" and move == "NW":
			valid = False
		if player.location == "NE" and move == "SW":
			valid = False
		if player.location == "SW" and move == "NE":
			valid = False
		return valid
	
	# Returns a list of moves the player can go to
	def moveOptions(self,player):
		returnVal = []
		for move in self.spaces:
			if self.validMove(player,move):
				returnVal.append(move)
		return returnVal

	# Moves a player to a position regardless if it is valid or not
	def movePlayer(self,player,move):
		# Find the player on the board and remove him/her if he/she exists
		for k in self.spaces:
			if self.spaces[k] == player:
				self.spaces[k] = None
		# Put the player into the space
		self.spaces[move] = player
	
	# Returns a dictionary representation of the object
	def toDict(self):
		return self.spaces

# Represents all players participating in the game
class PlayerList:
	def __init__(self):
		self.list = []
		self.gameboard = None 

	def __str__(self):
		returnStr = "Players: "
		for p in self.list:
			returnStr += str(p) + ", "
		return returnStr

	# Keep a reference of the gameboard, it will be used for
	# functions that deal between p2p and the gameboard itself
	# and the player
	def setGameboard(self,gameboard):
		self.gameboard = gameboard

	def getPlayerstates(self):
		returnVal = []
		for p in self.list:
			returnVal.append(p.getState())
		return returnVal

	def getCardLists(self):
		returnVal = []
		for p in self.list:
			returnVal.append({"playerId":p.playerId,"cardlist":p.getCards()})
		return returnVal

	def getMessages(self):
		returnVal = []
		for p in self.list:
			returnVal.append({"playerId":p.playerId,"message":p.getMessage()})
		return returnVal

	# Returns a list of dictionaries that contain playerId and choices
	# he/she can make
	def getMoveOptions(self):
		returnVal = []
		for p in self.list:
			returnVal.append({"playerId": p.playerId, "choices": self.gameboard.moveOptions(p)})
		return returnVal
		
	def addPlayer(self,playerId):
		self.list.append(Player(playerId))

	def movePlayer(self,playerId,choice):
		player = self.selectPlayer(playerId)
		if self.gameboard.validMove(player,choice):
			self.gameboard.movePlayer(player,choice)
			player.move(choice)
			player.updateMessage(None)
		else:
			player.updateMessage("Cannot move to that space")
		
	def selectPlayer(self,playerId):
		player = None
		for p in self.list:
			if p.playerId == playerId:
				player = p
		return player

# Represents a player
class Player:
	def __init__(self,playerId):
		self.playerId = playerId
		self.suspect = None
		self.location = None
		self.message = None
		self.cards = ["king","queen","jack","ace"]		
	
	def __str__(self):
		return self.playerId
	
	# Returns a list of cards the player holds
	def getCards(self):
		return self.cards
	
	# Returns the message string for the player UI
	def getMessage(self):
		return self.message
	
	# Updates the player's personal message
	def updateMessage(self,message):
		self.message = message
	
	# Returns a dict of the player specific state
	def getState(self):
		return {
			"playerId":self.playerId,
			"suspect":self.suspect
		}
	
	# Moves the player to a location in the gameboard
	def move(self,choice):
		self.location = choice
		