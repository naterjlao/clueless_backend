import random
import Entity


class Game(object):

	def __init__(self):

		self.players = dict()
		self.game_id = None
		self.game = None

	def add_player(self, name):

		self.players[name] = Entity.Player(name)

	def start_game(self):

		game_players = [self.players[key] for key in self.players]
		self.game = Entity.GameModel(self.game_id, game_players)

		card_deck = Cards()
		card_deck.shuffle_cards()
		self.game.win_hand = card_deck.deal_winning_cards()

		player_count = len(self.players)

		hands = card_deck.deal_cards(player_count)
		for x in range(player_count):
			self.game.players[x].game_cards = hands[x]


	def end_game(self):

		self.game = None
		self.players = dict()


	def make_move(self, player, suspect, room):

		self.check_user(player)
		self.check_turn(player)
		self.check_turn_status(Entity.AWAITING_MOVE)

		self.check_suspect(suspect)
		self.check_player_suspect(suspect)
		self.check_board(room)
		self.check_board_available(room)

		current_space = self.get_suspect_current_space(suspect)
		new_space = self.game.game_board[room]
		self.check_ifconnected(current_space, new_space)

		self.move_suspect(suspect, new_space)

		if isInstance(new_space, Entity.Room):
			self.game.turn_status = Entity.AWAITING_SUGGESTION
		else:
			self.game.turn_status = Entity.AWAITING_ACCUSATION_OR_END_TURN



	def select_suspect(self, name, suspect):

		self.check_suspect(suspect)
		self.players[name].suspect = suspect


	def make_suggestion(self, player, suspect, weapon, room):

		self.check_user(player)
		self.check_turn(player)
		self.check_suspect(suspect)
		self.check_weapon(weapon)
		self.check_room(room)
		self.check_suggestion_turn_status()
		self.check_suggestion_room(room)

		suggestion_room = self.game.game_board[room]
		self.move_suspect(suspect, suggestion_room)
		self.move_weapon(weapon, suggestion_room)

		self.game.current_suggestion = Entity.Suggestion(suspect, weapon, room)


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


	def make_accusation(self, player, suspect, weapon, room):

		self.check_user(player)
		self.check_turn(player)
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


	def end_turn(self, player):

		self.check_user(player)
		self.check_turn(player)
		self.check_end_turn_status()
		self.next_turn()




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

		if not move_available:
			self.game.turn_status = Entity.AWAITING_ACCUSATION_OR_END_TURN



	def next_player_index(self):
		turn_index = self.game.turn_lsit.index(self.game.current_player)
		if turn_index < (len(self.game.turn_list)-1):
			turn_index += 1
		else:
			turn_index = 0

		return turn_index


	def check_turn_status(self, status):
		if self.game.turn_status != status:
			raise SyntaxError

	def check_turn(self, player):
		if player != self.game.current_player.player:
			raise SyntaxError


	def check_end_turn_status(self):
		if self.game.turn_status != Entity.AWAITING_ACCUSATION_OR_END_TURN:
			raise SyntaxError




	'''
	Move Object Helpers	
	'''

	def check_room(self, room):
		if room not in Entity.ROOMS:
			raise

	def check_board_available(self, room):
		if not self.game.game_board[room].isAvailable():
			raise SyntaxError

	def check_board(self, room):
		if not self.game.game_board[room]:
			raise SyntaxError

	def check_ifconnected(self, current_space, new_space):
		if new_space.name not in current_space.connected:
			raise SyntaxError




	'''
	Suggestion Helpers	
	'''

	def move_suspect(self, suspect, suggestion_room):
		current_space = self.get_suspect_current_space(suspect)
		current_space.suspects.remove(suspect)
		suggestion_room.suspects.append(suspect)


	def move_weapon(self, weapon, room):

		current_room = self.get_weapon_current_space(weapon)
		current_room.weapons.remove(weapon)
		room.weapons.appednd(weapon)


	def get_weapon_current_space(self, weapon):

		game_board = self.game.game_board
		rooms = [room for room in [game_board[space]
				for space in game_board
				if isInstance(game_board[space], Entity.Room)]]

		for room in rooms:
			if weapon in room.weapons:
				return room

	def get_suspect_current_space(self, suspect):
		for space in self.game.game_board:
			if suspect in self.game.game_board[space].suspects:
				return self.game.game_board[space]


	def check_weapon(self, weapon):

		if weapon not in Entity.WEAPONS:
			raise SyntaxError


	def check_suspect(self, suspect):
		if suspect not in Entity.SUSPECTS:
			raise SyntaxError


	def check_player_suspect(self, suspect):
		if suspect != self.game.current_player.suspect:
			raise SyntaxError

	def check_user(self, name):

		for player in self.game.players:
			if name == player.name:
				return
		raise SyntaxError


	def check_card(self, card):

		valid_items = Entity.SUSPECTS
		valid_items += Entity.WEAPONS
		valid_items += Entity.ROOMS

		if card not in valid_items:
			raise SyntaxError

	def check_suggestion_card(self, card):
		cards = self.game.suggestion_response.game_cards
		player_items = [ card.item for card in cards]

		if card not in player_items:
			raise SyntaxError



	def check_suggestion_room(self, room):
		suspect = self.game.current_player.suspect
		if suspect not in self.game.game_board[room].suspects:
			raise SyntaxError


	def check_suggestion_player(self, player):
		if player != self.game.suggestion_response.player:
			raise SyntaxError

	def check_suggestion_turn_status(self):
		if self.game.turn_status != Entity.AWAITING_SUGGESTION:
			raise SyntaxError








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

	def shuffle_cards(self):
		random.shuffle(self.game_cards)

	def deal_cards(self, hands):
		return [self.game_cards[x::hands] for x in range(hands)]

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

