#!/usr/bin/python3

# Set up Constants for Characters, Rooms, Names and Turns Variables

SUSPECT = 'Suspect'
MUSTARD = 'Colonel Mustard'
SCARLET = 'Miss Scarlet'
PLUM = 'Professor Plum'
GREEN = 'Mr Green'
WHITE = 'Mrs White'
PEACOCK = 'Mrs Peacock'

SUSPECTS = [MUSTARD, SCARLET, PLUM, GREEN, WHITE, PEACOCK]

WEAPON = 'Weapon'
ROPE = 'Rope'
LEAD_PIPE = 'Lead Pipe'
KNIFE = 'Knife'
WRENCH = 'Wrench'
CANDLESTICK = 'Candlestick'
REVOLVER = 'Revolver'

WEAPONS = [ROPE,LEAD_PIPE,KNIFE,WRENCH,CANDLESTICK,REVOLVER]

ROOM = 'Room'
KITCHEN = 'Kitchen'
BALLROOM = 'Ballroom'
CONSERVATORY = 'Conservatory'
BILLIARD_ROOM = 'Billiard Room'
LIBRARY = 'Library'
STUDY = 'Study'
HALL = 'Hall'
LOUNGE = 'Lounge'
DINING_ROOM = 'Dining Room'

ROOMS = [KITCHEN,BALLROOM,CONSERVATORY,BILLIARD_ROOM,LIBRARY,STUDY,HALL,LOUNGE,DINING_ROOM]

STUDY_LIBRARY = 'study-library Passage'
STUDY_HALL = 'study-hall Passage'
HALL_BILLIARD = 'hall-billiard Passage'
HALL_LOUNGE = 'hall-lounge Passage'
LOUNGE_DINING = 'lounge-dining Passage'
LIBRARY_CONSERVATORY = 'library-conservatory Passage'
LIBRARY_BILLIARD = 'library-billiard Passage'
BILLIARD_BALLROOM = 'billiard-ballroom Passage'
BILLIARD_DINING = 'billiard-dining Passage'
DINING_KITCHEN = 'dining-kitchen Passage'
CONSERVATORY_BALLROOM = 'conservatory-ballroom Passage'
BALLROOM_KITCHEN = "ballroom-kitchen Passage"

Passages = [STUDY_LIBRARY,STUDY_HALL,
			HALL_BILLIARD,HALL_LOUNGE,
			LOUNGE_DINING,
			LIBRARY_CONSERVATORY, LIBRARY_BILLIARD,
			BILLIARD_BALLROOM, BILLIARD_DINING,
			DINING_KITCHEN,
			CONSERVATORY_BALLROOM,
			BALLROOM_KITCHEN
			]

AWAITING_MOVE = "Awaiting Move"
AWAITING_SUGGESTION = "Awaiting Suggestion"
AWAITING_SUGGESTION_RESPONSE = "Awaiting Response"
AWAITING_ACCUSATION_OR_END_TURN = "Awaiting Accusation or End of Turn"


# Player Class is for each Player in Game

class Player(object):

	def __init__(self, name, suspect = None, card_hand = None, card_seen = None):

		self.name = name

		if suspect:
			self.suspect = suspect
		else:
			self.suspect = None
		if card_hand:
			self.card_hand = card_hand
		else:
			self.card_hand = list()
		if card_seen:
			self.card_seen = card_seen
		else:
			self.card_seen = list()


	def format(self):

		return{
			"user": self.name,
			"suspect": self.suspect,
			"card_hand": [game_card.format() for game_card in self.card_hand],
			"card_seen:": [game_card.format() for game_card in self.card_seen]
		}


# Card Class for each Card Item (Weapon, Character, Room)
class Card(object):

	def __init__(self, item, item_type):
		self.item = item
		self.type = item_type

	def format(self):
		return {
			"item": self.item,
			"item_type": self.type,
		}

# Suggestion Class for both Suggestions and Accusations
class Suggestion(object):

	def __init__(self, suspect, weapon, room):

		self.weapon = weapon
		self.suspect = suspect
		self.room = room

	def format(self):

		return{
			"suspect": self.suspect,
			"weapon": self.weapon,
			"room": self.room
		}

# BoardObject is interface for Rooms, Passages, HomeSpaces

class BoardObject(object):

	def __init__(self, name, connected, suspects = None):

		self.name = name
		self.connected = connected
		if suspects:
			self.suspects = suspects
		else:
			self.suspects = list()


	#Availability Rules differ by BoardObject Type
	def available(self):
		pass

	def format(self):

		return {
			"name": self.name,
			"connected": self.connected,
			"suspects": self.suspects
		}


#Room Class for Room BoardObject
class Room(BoardObject):

	def __init__(self, name, connected, suspects = None, weapons = None):

		super(Room, self).__init__(name, connected, suspects)

		if weapons:
			self.weapons = weapons
		else:
			self.weapons = list()

	# Multiple Players can be in Room
	def available(self):
		pass

	def format(self):

		return {
				"name": self.name,
				"connected": self.connected,
				"suspects": self.suspects,
				"weapons": self.weapons
		}



class Passage(BoardObject):

	def __init__(self, name, connected, suspects = None):

		super(Passage, self).__init__(name, connected, suspects)

	#Only One Player in Passage at a Time
	def available(self):
		return not self.suspects


class HomeSpace(BoardObject):

	def __init__(self, name, connected, suspects = None):
		super(HomeSpace, self).__init__(name, connected, suspects)

	#Return False since this is not an available Space after first Move
	def available(self):
		return False

# GameModel Class formats a GameModel Dictionary to be used in GameModelBuilder class

class GameModel(object):

	def __init__(self, game, players, player_messages = None,
				 turn_list = None, current_player = None, turn_status = None,
				 current_suggestion = None, suggestion_response = None,
				 win_hand = None, game_active = True, game_winner = None,
				 game_board = None):

		self.game = game

		self.players = players

		if player_messages:
			self.player_messages = player_messages
		else:
			self.player_messages = list()

		if turn_list:
			self.turn_list = turn_list
		else:
			self.turn_list = list(players)

		if current_player:
			self.current_player = current_player
		else:
			self.current_player = self.turn_list[0]

		if turn_status:
			self.turn_status = turn_status
		else:
			self.turn_status = AWAITING_MOVE

		self.current_suggestion = current_suggestion

		self.suggestion_response = suggestion_response

		if win_hand:
			self.win_hand = win_hand
		else:
			self.win_hand = list()

		self.game_active = game_active

		self.game_winner = game_winner

		if game_board:
			self.game_board = game_board

		else:
			self.game_board = {

				KITCHEN: Room(name=KITCHEN, connected=[ DINING_KITCHEN, BALLROOM_KITCHEN, STUDY],weapons=[ROPE]),

				BALLROOM: Room( name=BALLROOM, connected=[ BALLROOM_KITCHEN, CONSERVATORY_BALLROOM,BILLIARD_BALLROOM],weapons=[LEAD_PIPE]),

				CONSERVATORY: Room(name=CONSERVATORY, connected=[CONSERVATORY_BALLROOM, LIBRARY_CONSERVATORY,LOUNGE], weapons=[CANDLESTICK]),

				BILLIARD_ROOM: Room(name=BILLIARD_ROOM,connected=[HALL_BILLIARD,LIBRARY_BILLIARD,BILLIARD_BALLROOM,BILLIARD_DINING],weapons=[KNIFE]),

				LIBRARY: Room(name=LIBRARY,connected=[STUDY_LIBRARY,LIBRARY_CONSERVATORY, LIBRARY_BILLIARD], weapons=[WRENCH]),

				STUDY: Room(name = STUDY,connected = [KITCHEN,STUDY_LIBRARY, STUDY_HALL], weapons = [REVOLVER]),

				HALL: Room( name = HALL,connected = [STUDY_HALL,HALL_BILLIARD, HALL_LOUNGE]),

				LOUNGE: Room( name = LOUNGE, connected = [CONSERVATORY, HALL_LOUNGE,LOUNGE_DINING]),

				DINING_ROOM: Room(name=DINING_ROOM, connected=[LOUNGE_DINING, BILLIARD_DINING, DINING_KITCHEN]),

				STUDY_LIBRARY: Passage(name = STUDY_LIBRARY, connected=[STUDY, LIBRARY]),

				STUDY_HALL: Passage(name=STUDY_HALL,connected=[ STUDY, HALL]),

				HALL_BILLIARD: Passage(name=HALL_BILLIARD, connected=[HALL, BILLIARD_ROOM]),

				HALL_LOUNGE: Passage( name = HALL_LOUNGE,connected =[HALL,LOUNGE]),

				LOUNGE_DINING: Passage( name=LOUNGE_DINING,connected=[ LOUNGE, DINING_ROOM]),

				LIBRARY_CONSERVATORY: Passage( name=LIBRARY_CONSERVATORY, connected=[ LIBRARY,CONSERVATORY]),

				LIBRARY_BILLIARD: Passage(name=LIBRARY_BILLIARD, connected=[LIBRARY,BILLIARD_ROOM]),

				BILLIARD_BALLROOM: Passage(name=BILLIARD_BALLROOM, connected=[BILLIARD_ROOM,BALLROOM]),

				BILLIARD_DINING: Passage(name = BILLIARD_DINING, connected = [BILLIARD_ROOM,DINING_ROOM]),

				DINING_KITCHEN: Passage(name=DINING_KITCHEN, connected=[DINING_ROOM,KITCHEN] ),

				CONSERVATORY_BALLROOM: Passage(name = CONSERVATORY_BALLROOM, connected = [CONSERVATORY, BALLROOM]),

				BALLROOM_KITCHEN: Passage(name = BALLROOM_KITCHEN, connected = [BALLROOM,KITCHEN]),

				MUSTARD: HomeSpace(name = MUSTARD, connected=[LOUNGE_DINING], suspects=[MUSTARD]),

				SCARLET: HomeSpace(name = SCARLET,connected=[HALL_LOUNGE], suspects=[SCARLET]),

				PLUM: HomeSpace(name = PLUM, connected = [STUDY_LIBRARY], suspects=[PLUM]),

				GREEN: HomeSpace(name= GREEN, connected = [CONSERVATORY_BALLROOM], suspects=[GREEN]),

				WHITE: HomeSpace(name = WHITE, connected = [BALLROOM_KITCHEN], suspects=[WHITE]),

				PEACOCK: HomeSpace(name = PEACOCK, connected = [LIBRARY_CONSERVATORY], suspects=[PEACOCK])
				}


	# Returns a dictionary of the current game state.
	def format(self):

		return {

			"game": self.game,

			"players": [player.format() for player in self.players],

			"player_messages": self.player_messages,

			'turn_list': [player.format() for player in self.turn_list],

			"current_player": self.current_player.format(),

			"turn_status": self.turn_status,

			"current_suggestion": self.current_suggestion.format()
				if self.current_suggestion else None,

			"suggestion_response": self.suggestion_response.format()
				if self.suggestion_response else None,

			"win_hand": [card.format() for card in self.win_hand],

			"game_active": self.game_active,

			"game_winner": self.game_winner.format()
				if self.game_winner else None,

			"game_board": {

				key:(self.game_board[key]).format()
					for key in self.game_board
			}
		}

# GameModelBuilder Class builds upon GameModel Dictionary and will be ultimately used/instantiated in our Server Class

class GameModelBuilder(object):

	def build_game(self, game_state):

		game_state = game_state.copy()

		game_state["players"] = self.build_players(game_state["players"])

		game_state["turn_list"] = [

			player for player in game_state["players"]
			if player.name in [
				turn_list_player["user"]
				for turn_list_player in game_state["turn_list"]
			]
		]

		if game_state["current_player"]:
			game_state["current_player"] = [player for player in game_state["players"]
				if player.name == game_state["current_player"]["name"]][0]

		game_board = dict()

		for key in game_state["game_board"]:

			if key in ROOMS:
				game_board[key] = Room(**game_state["game_board"][key])
			if key in Passages:
				game_board[key] = Passage(**game_state["game_board"][key])
			if key in SUSPECTS:
				game_board[key] = HomeSpace(**game_state["game_board"][key])

		game_state["game_board"] = game_board

		return [GameModel(**game_state)]


	def build_game_cards(self, game_cards):

		return [Card(**game_card_dict) for game_card_dict in game_cards]


	def build_players(self, players):

		for player_dict in players:
			player_dict["card_hand"] = self.build_game_cards(
				player_dict["card_hand"])
			player_dict["card_seen"] = self.build_game_cards(
				player_dict["card_seen"])

		return [Player(**player_dict) for player_dict in players]


