#!/usr/bin/python3
import random
import Entity
import json
import ErrorServer
import LogServer

LOG = LogServer.logger(__name__)


# Defines the Game interface
# This is the only thing that should be imported when interfacing with the Cluless game.
class Game(object):

	def __init__(self):

		self.players = dict()
		self.game_id = None
		self.game = None   # This is a GameModel

	# Returns the gamestate dictionary object on demand.
	# This is utilized by the Serverside which is pushed in JSON payload
	def getGamestate(self):
		gamestate = {}
		
		# The game instance variable would not be intialized until
		# some function is called, spoof the client for now
		if (self.game == None):
			game = Entity.GameModel(["temporary"],["workaround"])
		else:
			game = self.game

		# Return the dictionary reprsentation of the game.
		gamestate["currentPlayerId"] = game.current_player
		gamestate["turnStatus"] = game.turn_status
		gamestate["suggestionCharacter"] = self.game.suggestion_response.suspect

		
		gamestate["availableCharacters"] = self.get_available_characters()
		
		return gamestate

	# Returns a dictionary object where:
	# Key: a Room
	# Value: the list of players in the room or none
	def getGameboard(self):
		gameboard = {}
		if (self.game != None):
			for position in self.game.game_board:
				gameboard[position] = self.game.game_board[position]
		return gameboard

	# Returns a list of dictionary objects for each player
	def getPlayerstates(self):
		playerstates = []
		if (self.players != None):
			for name in self.players:
				payload = {}
				payload["playerId"] = name
				payload["suspect"] = self.players[name].suspect
				#payload["isSuggestionValid"] = False #self.check_suggestion_turn_status() # TODO I am guessing this is a bool
				payload["isSuggestionValid"] = self.game.turn_status #IF turn_status  Awaiting_Suggestion_Response TRUE, ELSE FALSE

				state = {}
				state["playerId"] = name
				state["payload"] = payload
				
				playerstates.append(state)
		
		return playerstates
	
	# Returns a list
	# Within the list are dictionaries
	# Each dictionary must have:
	# - playerId : string
	# - payload : dict
	# Within payload:
	# - choices: a list of strings that the playerId can go to based on the current state
	# The list contains the dictionaries for ALL registered players
	def getMoveOptions(self):
		moveOptions = []
		if (self.players != None and self.game != None):
			for playerId in self.players:
				
				# Get the list of available postions the player can go to
				choices = list()
				current_space = self.get_suspect_current_space(playerId)				
				for room in self.game.game_board[current_space].connected: 
					if self.game.game_board[room].available(): 
						choices.insert(0,room)

				payload = {"choices": choices} # the playload is a singleton with only choices
				playerOption = {}
				playerOption["playerId"] = playerId
				playerOption["payload"] = payload
				moveOptions.append(playerOption) # add to the dict list
		return moveOptions
		
	def getSuggestionOptions(self):
		
		for playerId in self.players:	
			current_space = self.get_suspect_current_space(playerId)				
			get_suggestion_options(current_space)
		
				
		x = self.game.format()
		for player in x["players"]: 
			
			return ({

			"user": player["user"],
			"card_hand": player["suggestion_options"]

			})
		
		'''
		# copied from check_suggestion_options
		suggestion_options = list()
		room = self.game.game_board[current_space].name
		self.game.current_player.suggestion_options.insert(0,room)

		for suspect in Entity.SUSPECTS: 
			self.game.current_player.accusation_options.insert(0,suspect)
	
		for weapon in Entity.WEAPONS: 
			self.game.current_player.accusation_options.insert(0,weapon)

		return self.game.current_player.suggestion_options
		'''
		
	def getAccusationOptions(self):
		
		get_accusation_options()
		
		x = self.game.format()
		for player in x["players"]: 
			
			return ({

			"user": player["user"],
			"card_hand": player["accusation_options"]

			})
		
		'''
		accusation_options = list()		
		for weapon in Entity.WEAPONS: 
			self.game.current_player.accusation_options.insert(0,weapon)
		for room in Entity.ROOMS: 
			self.game.current_player.accusation_options.insert(0,room)
		for suspect in Entity.SUSPECTS: 
			self.game.current_player.accusation_options.insert(0,suspect)
		
		return self.game.current_player.accusation_options
		'''
		
	def getChecklists(self):
		
		x = self.game.format()
		for player in x["players"]: 
			
			return ({

			"user": player["user"],
			"card_hand": player["card_seen"]

			})
		
		
	def getCardlists(self):
	
		x = self.game.format()
		for player in x["players"]: 
			
			return ({

			"user": player["user"],
			"card_hand": player["card_hand"]

			})
		

	def getMessages(self):

		x = self.game.format()
		for player in x["players"]: 
			
			return ({

			"user": player["user"],
			"card_hand": player["messages"]

			})
		
		
	# This does nothing, but keep this here to catch the import call
	def enteredGame(self,playerId):
		pass
	
	# Moves the <playerId> to the <choice> position
	# If the player can move to the position, the game updates accordingly
	# If the player cannot move to the position, the player's message field is updated and no updates are made
	# Return nothing
	def selectMove(self,playerId,choice):
		# observe that make_move needs playerId, suspect and choice
		# the frontend is only giving us playerId and choice
		suspect = self.players[playerId].suspect
		self.make_move(playerId,suspect,choice)


	def selectCard(self,playerId,choice):
		pass # TODO - what is this supposed to do? 
		

	def disproveSuggestion(self,playerId,card,type,cannotDisprove):
		pass # TODO 
	


	def disproveAccusation(self,playerId,card,type,cannotDisprove):
		pass # UNNECESSARY
			
    # Adds a player with a given name
    # The <name> is used as identifier for the player.
    # This function MUST be called before start_game()
	def add_player(self, name):
		self.players[name] = Entity.Player(name)

	def remove_player(self, playerId): #NOTE - took out playerId
		pass # DISABLE BC BROKEN / LEAVE OUT UNTIL AFTER MOVEMENT TESTED
		'''
		self.game.turn_list.remove(playerId)
	
		'''
    # Initiates the start of the game.
    # Cards are given out to each of the players
	def start_game(self):

		game_players = [self.players[key] for key in self.players]
		self.game = Entity.GameModel(self.game_id, game_players)

		card_deck = Cards()
		card_deck.shuffle_cards()
		self.game.win_hand = card_deck.deal_winning_cards()

		player_count = len(self.players)

		hands = card_deck.deal_cards(player_count)
		for x in range(player_count):
			self.game.players[x].card_hand = hands[x]

		LOG.info("started game")


		#print(json.dumps(self.game.format(), indent=2))

    # Wipes out the game instance and clears the players held
	def end_game(self):
		self.game = None
		self.players = dict()

		LOG.info("ended game")


    # Performs a movement for the player
    # Params:
    # <name> : player identifier
    # <suspect> : the suspect of the player
    # <room> : move destination
	def make_move(self, name, suspect, room):

		self.check_user(name)
		self.check_turn(name)
		self.check_turn_status(Entity.AWAITING_MOVE)

		
		self.check_move_options(room)

			
		self.check_suspect(suspect)
		self.check_player_suspect(suspect)
		self.check_board(room)
		self.check_board_available(room)



		current_space = self.get_suspect_current_space(suspect)
		new_space = self.game.game_board[room]
		self.check_ifconnected(current_space, new_space)

		self.move_suspect(suspect, new_space)

		if isinstance(new_space, Entity.Room):
			self.game.turn_status = Entity.AWAITING_SUGGESTION
			
			msg = "{0} to make a suggestion".format(name)
			self.sendMsgtoAll(msg)

		else:
			self.game.turn_status = Entity.AWAITING_ACCUSATION_OR_END_TURN
			
			msg = "{0} to make an accusation or end".format(name)
			self.sendMsgtoAll(msg)
		#json.dumps(self.game.format(), indent=2)

		LOG.info("player made a board move: ")


    #DEPRECATE in favor of select_character
	def select_suspect(self, name, suspect):
		self.check_suspect(suspect)
		self.players[name].suspect = suspect

	# Returns a list of the CURRENT available characters in the game
	def get_available_characters(self):
		return Entity.CHARACTERS

	# Associates a suspect character for the given <name> of the player.
	def select_character(self, name, suspect):

		self.check_character(suspect)
		self.players[name].suspect = suspect
		Entity.CHARACTERS.remove(suspect)
		
		available_characters = {"available_characters": Entity.CHARACTERS}
		return available_characters

	#Helper for select_character
	def check_character(self, suspect):
		if suspect not in Entity.CHARACTERS:
			raise ErrorServer.InvalidMove

    # Performs a make a suggestion call
    # <name> : player identifier of the person making the suggestion
    # <suspect> : the suspect that is called out in the suggestion
    # <weapon> : the weapon that is called out in the suggestion
    # <room> : the room that is called out in the suggestion

    
    # gamestate.turn_status is changed to AWAITING_SUGGESTION_RESPONSE
    # gamestate.check_suggestion_player is assigned PlayerId and they must respond to suggestion
    # next see suggestion_response method below


	def make_suggestion(self, name, suspect, weapon, room):

		self.check_user(name)
		self.check_turn(name)
		self.check_suspect(suspect)
		self.check_weapon(weapon)
		self.check_room(room)
		self.check_suggestion_turn_status()
		self.check_suggestion_room(room)

		suggestion_room = self.game.game_board[room]
		self.move_suspect(suspect, suggestion_room)
		self.move_weapon(weapon, suggestion_room)

		self.game.current_suggestion = Entity.Suggestion(suspect, weapon, room)

		suggestion_responder = self.check_suggestion_responder()

		#self.game.suggestion_response_player = response_player
		if suggestion_responder:
			self.game.check_suggestion_player = suggestion_responder
			self.game.turn_status = Entity.AWAITING_SUGGESTION_RESPONSE

		else:
			self.game.turn_status = Entity.AWAITING_ACCUSATION_OR_END_TURN

		LOG.info("player made a suggestion move: ")


	#Helps make_move
	# Checks to see who can resopnd to the Suggestion
	def check_suggestion_responder(self):

		for player in self.game.players:
			if player.name is self.game.current_suggestion.suspect:
				LOG.info("the suggested is in the game so should move to AWAITING SUGGESTION RESPONE")
				return player
			else:
				LOG.info("the suggested player isn't in the game so pass")
				return None



    # Performs a counter response to the suggestion
    # <player> : the player performing the counter
    # <card> : the card used for countering the suggestion

	def respond_suggestion(self, player, card):

		self.check_user(player)
		self.check_suggestion_player(player)
		self.check_card(card)
		self.check_suggestion_card(card)

		if card in Entity.WEAPONS:
			item_type = Entity.WEAPON
		elif card in Entity.ROOMS:
			item_type = Entity.ROOM
		else:
			item_type = Entity.SUSPECT

		cards = Entity.Card(card, item_type)

		self.game.current_player.card_seen.append(cards)

		self.game.turn_status = Entity.AWAITING_ACCUSATION_OR_END_TURN


		LOG.info("player responded to a suggestion: ")


    # Performs a make a accusation action
    # See make_suggestion() for parameter info.
	def make_accusation(self, name, suspect, weapon, room):


		self.check_user(name)
		self.check_turn(name)
		self.check_suspect(suspect)
		self.check_weapon(weapon)
		self.check_room(room)


		accusation = [suspect, weapon, room]
		winning_cards = [card.item for card in self.game.win_hand]
		if set(accusation) == set(winning_cards):
			self.game.game_active = False
			self.game.game_winner = self.game.current_player

		else:
			lost_player = self.game.current_player
			self.next_turn()
			self.game.turn_list.remove(lost_player)


		LOG.info("player made an accusation: ")




    # Ends the turn of the current player.
	def end_turn(self, name):

		self.check_user(name)
		self.check_turn(name)
		self.check_end_turn_status()
		self.next_turn()


		#print(json.dumps(self.game.format(), indent=2))


		LOG.info("player ended their turn ")



	# Returns a list of available connected rooms based on the current space
	def check_move_options(self, current_space):
		
		move_options = list()
		
		for room in self.game.game_board[current_space].connected: 
			if self.game.game_board[room].available(): 
				move_options.insert(0,room)

		return move_options

		#If need to rollback then just 
		#return self.game.game_board[current_space].connected


	'''
	Turn Queue Helpers
	'''
	def next_turn(self):

		turn_index = self.game.turn_list.index(self.game.current_player)
		if turn_index < (len(self.game.turn_list)-1):
			turn_index += 1
		else:
			turn_index = 0
		self.game.current_player = self.game.turn_list[turn_index]

		self.game.turn_status = Entity.AWAITING_MOVE

		current_space = self.get_suspect_current_space(self.game.current_player.suspect)
		move_available = False

		for space in current_space.connected:
			if self.game.game_board[space].available():
				move_available = True

		LOG.info("Please make a move")


		if not move_available:
			LOG.info("unable to make that move")
			self.game.turn_status = Entity.AWAITING_ACCUSATION_OR_END_TURN



	def next_player_index(self):
		turn_index = self.game.turn_list.index(self.game.current_player)
		if turn_index < (len(self.game.turn_list)-1):
			turn_index += 1
		else:
			turn_index = 0

		return turn_index


	# Checks turn status to make sure the right move is being performed at the right time
	def check_turn_status(self, status):
		if self.game.turn_status != status:
			raise ErrorServer.InvalidEndTurn
		#print(json.dumps(self.game.turn_status))
		return self.game.turn_status


	# Checks that the player making the move is 
	def check_turn(self, name):
		if name != self.game.current_player.name:
			raise ErrorServer.InvalidTurnList

	#Checks that the turn status is in the ending state, otherwise forces player to make a different move
	def check_end_turn_status(self):
		if self.game.turn_status != Entity.AWAITING_ACCUSATION_OR_END_TURN:
			raise ErrorServer.InvalidEndTurn


	'''
	Move Object Helpers	
	'''

	def check_room(self, room):
		if room not in Entity.ROOMS:
			raise ErrorServer.InvalidMove

	#Checks that the room is available. 
	#This would return False if the Hallway is full
	def check_board_available(self, room):
		if not self.game.game_board[room].available():
			raise ErrorServer.InvalidMove

	def check_board(self, room):
		if not self.game.game_board[room]:
			raise ErrorServer.InvalidMove

	#Checks that the room is connected
	def check_ifconnected(self, current_space, new_space):
		if new_space.name not in current_space.connected:
			raise ErrorServer.InvalidMove



	'''
	Suggestion Helpers	
	'''

	# Suspect moves to the current room when involved in a Suggestion
	def move_suspect(self, suspect, suggestion_room):
		current_space = self.get_suspect_current_space(suspect)
		current_space.suspects.remove(suspect)
		suggestion_room.suspects.append(suspect)

	# Weapon moves to the current room when involved in a Suggestion
	def move_weapon(self, weapon, room):

		current_room = self.get_weapon_current_space(weapon)
		current_room.weapons.remove(weapon)
		room.weapons.append(weapon)

	# Weapon moves to the current room when involved in a Suggestion
	def get_weapon_current_space(self, weapon):

		game_board = self.game.game_board
		rooms = [room for room in [game_board[space] # FIXME syntax is wrong
				for space in game_board
				if isinstance(game_board[space], Entity.Room)]]

		for room in rooms:
			if weapon in room.weapons:
				return room

	# Weapon moves to the current room when involved in a Suggestion
	def get_suspect_current_space(self, suspect):
		for space in self.game.game_board:
			if suspect in self.game.game_board[space].suspects:
				return self.game.game_board[space]


	def check_weapon(self, weapon):

		if weapon not in Entity.WEAPONS:
			raise ErrorServer.InvalidCard

	def check_suspect(self, suspect):
		if suspect not in Entity.SUSPECTS:
			raise ErrorServer.InvalidCard

	#Checks that make_move is moving the correct playerIds Character
	def check_player_suspect(self, suspect):
		if suspect != self.game.current_player.suspect:
			raise ErrorServer.InvalidSuspect

	# check_user checks if player exists, returns either Nothing or Error 
	def check_user(self, name):

		for player in self.game.players:
			if name == player.name:
				return 
		raise ErrorServer.InvalidSuspect


	def check_card(self, card):

		valid_items = Entity.SUSPECTS
		valid_items += Entity.WEAPONS
		valid_items += Entity.ROOMS

		if card not in valid_items:
			raise ErrorServer.InvalidCard


	def check_suggestion_card(self, card):
		cards = self.game.suggestion_response.game_cards
		player_items = [ card.item for card in cards]

		if card not in player_items:
			raise ErrorServer.InvalidCard


	def check_suggestion_room(self, room):
		suspect = self.game.current_player.suspect
		if suspect not in self.game.game_board[room].suspects:
			raise ErrorServer.InvalidSuggestion


	def check_suggestion_player(self, player):
		if player != self.game.suggestion_response.player:
			raise ErrorServer.InvalidSuggestion


	def check_suggestion_turn_status(self):
		if self.game.turn_status != Entity.AWAITING_SUGGESTION:
			raise ErrorServer.InvalidSuggestion

	def get_accusation_options(self):

		accusation_options = list()
		
		for weapon in Entity.WEAPONS: 
			self.game.current_player.accusation_options.insert(0,weapon)

		for room in Entity.ROOMS: 
			self.game.current_player.accusation_options.insert(0,room)

		for suspect in Entity.SUSPECTS: 
			self.game.current_player.accusation_options.insert(0,suspect)
		
		
		#return self.game.current_player.accusation_options

	
	def get_suggestion_options(self, current_space):
			
		suggestion_options = list()
		room = self.game.game_board[current_space].name
		self.game.current_player.suggestion_options.insert(0,room)

		for suspect in Entity.SUSPECTS: 
			self.game.current_player.accusation_options.insert(0,suspect)
	
		for weapon in Entity.WEAPONS: 
			self.game.current_player.accusation_options.insert(0,weapon)

		#return self.game.current_player.suggestion_options



	def get_accusation_options(self):

		accusation_options = list()
		
		for weapon in Entity.WEAPONS: 
			self.game.current_player.accusation_options.insert(0,weapon)

		for room in Entity.ROOMS: 
			self.game.current_player.accusation_options.insert(0,room)

		for suspect in Entity.SUSPECTS: 
			self.game.current_player.accusation_options.insert(0,suspect)
		
		
			return self.game.current_player.accusation_options

	
	def get_suggestion_options(self, current_space):
			
		suggestion_options = list()
		room = self.game.game_board[current_space].name
		self.game.current_player.suggestion_options.insert(0,room)

		for suspect in Entity.SUSPECTS: 
			self.game.current_player.accusation_options.insert(0,suspect)
	
		for weapon in Entity.WEAPONS: 
			self.game.current_player.accusation_options.insert(0,weapon)

		return self.game.current_player.suggestion_options



	#OPTIONAL - if needed for Frontend Buttons in Accusations or Suggestions
	def get_weapons_list(self): 

        	return Entity.WEAPONS


	#OPTIONAL - if needed for Frontend Buttons in Accusations or Suggestions
	def get_rooms_list(self): 

			return Entity.ROOMS


	#OPTIONAL - if needed for Frontend Buttons in Accusations or Suggestions
	def get_suspects_list(self): 

			return Entity.SUSPECTS


	#Returns Cards in the players Hand
	def get_player_card_hand(self): 

		return self.game.current_player.card_hand
		#print(self.game.current_player.card_seen)


	#Returns what Cards a player has seen via Suggestions
	def get_player_card_seen(self): 

		return self.game.current_player.card_seen
		#print(self.game.current_player.card_hand)
		#print(self.game.game_board)



	#add messages to all player.messages
	def sendMsgtoAll(self, msg): 

		for player in self.game.players:
			player.messages.insert(0,msg)

	#add messages to all current_player.messages
	def sendMsgtoOne(self, msg): 

		self.game.current_player.messages.insert(0,msg)







class Cards(object):


	def __init__(self):

		self.suspects = [
			Entity.Card(item = item, item_type = Entity.SUSPECT)
			for item in Entity.SUSPECTS]

		self.weapons = [
			Entity.Card(item = item, item_type = Entity.WEAPON)
			for item in Entity.WEAPONS]

		self.rooms = [
			Entity.Card(item = item, item_type = Entity.ROOM)
			for item in Entity.ROOMS]

		self.game_cards = self.suspects + self.weapons + self.rooms

		self.winning_cards = list()


	#Shuffles cards 
	def shuffle_cards(self):
		random.shuffle(self.game_cards)

	#Deals Cards to player
	def deal_cards(self, hands):
		return [self.game_cards[x::hands] for x in range(hands)]

	#Selects a random set of Cards as part of Winning Hand Deck
	def deal_winning_cards(self):

		win_suspect = self.suspects[random.choice(range(len(self.suspects)))]

		win_weapon = self.weapons[random.choice(range(len(self.weapons)))]

		win_room = self.rooms[random.choice(range(len(self.rooms)))]

		self.winning_cards = [win_suspect, win_weapon, win_room]

		self.game_cards = [
			game_card for game_card in self.game_cards
			if game_card not in self.winning_cards
		]

		return self.winning_cards



	
	
