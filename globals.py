#!/usr/bin/python3
################################################################################
# File:            globals.py
# Subcomponent:    Clueless/Backend
# Language:        python3
# Author:          Nate Lao (nlao1@jh.edu)
# Date Created:    4/28/2020
# Description:
#          Contains immutable values to be used in the Backend subcomponents.
#
################################################################################

################################################################################
# ADMINISTRATION
################################################################################
LOG_FILE='/opt/clueless/log/backend.log'
DEBUG=False 						# Set to false before deployment!
PLAYER_ID='playerId'
DIRTY='dirty'
PAYLOAD='payload'
LOCATION='location'

################################################################################
# GAME VARIABLES
################################################################################

# Minimal number of players to play the game
MIN_PLAYERS = 2
MAX_PLAYERS = 6

# Game status values
STATE_INITIAL = "INITIAL"			# Indicates that the game has not started, players are not set at this point
STATE_STARTED = "STARTED"			# Indicates that the game is in progress, players are able to move on the board
STATE_SUGGESTION = "SUGGESTION"		# Indicates that the game is in a state of suggestion, certain events must occur in order to return to STARTED
STATE_ACCUSATION = "ACCUSATION"		# Indicates that the game is in a state of accusation, certain events must occur in order to return to STARTED
STATE_END = "END"					# Indicates that the game has ended. No more actions may occur

# Player status values
PLAYER_INITIAL  = "INITIAL"			# The player is ready to play
PLAYER_IN_PLAY  = "IN_PLAY"			# The player is in movement state
PLAYER_SUGGEST  = "SUGGEST"			# The player must make a suggestion
PLAYER_ACCUSE   = "ACCUSE"			# The player must make an accusation
PLAYER_DEFEND   = "DEFEND"			# The player must return a defense to the accusation or suggestion
PLAYER_WIN      = "WIN"				# The player has won the game, the game should be at the END state
PLAYER_LOSE     = "LOSE"			# The player has lost the game and may no longer progress

CARD_UNASSIGNED = "UNASSIGNED"		# The card is currently held by a player or case file
CARD_CASE_FILE  = "CASE_FILE"		# The card is held by the case file

# String list of room names
# The way that the list is stylized resembles the actual
# board setup. The number of rooms must be a result of a
# number that is raised to a factor of 2 (a square).
ROOMS = [	'Study', 'Hall', 'Lounge',
			'Library', 'Billiard Room', 'Dining Room',
			'Conservatory','Ballroom','Kitchen'
		]

# String list of default suspects and initial positions
# Miss Scarlet is set to the first index due to precedence before everyone else
SUSPECTS = ['Miss Scarlet','Colonel Mustard','Mrs White','Mr Green','Mrs Peacock','Professor Plum']
INITIAL  = [(1,2),(2,5),(7,8),(6,7),(3,6),(0,3)] # These are based on indices on the ROOMS, ordered the same a SUSPECTS

# String list of weapons
WEAPONS = ['Candlestick','Knife','Lead Pipe','Revolver','Rope','Wrench']

# List of tuples that represent the secret passages the player can take
# A passage cannot be occupied by a player. ie. the Player shall not
# have a location state of a "secret passage", rather the Player
# "warped" to the connecting room. Secret passages are bi-directional.
# A player may start at elem[0] and end in elem[1] and vice-versa.
SECRET_PASSAGES = [(ROOMS[0],ROOMS[8]),(ROOMS[2],ROOMS[6])]
				 #[("Study","Kitchen"),("Lounge","Conservatory")]

# Cards are comprised of all suspects, weapons and rooms.
CARDS = SUSPECTS + ROOMS + WEAPONS
