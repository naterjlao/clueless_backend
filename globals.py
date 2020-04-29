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

# String list of default suspects
SUSPECTS = ['Colonel Mustard','Miss Scarlet', 'Professor Plum',' Mr. Green', ' Mrs. White', 'Mrs. Peacock']

# String list of weapons
WEAPONS = ['Candlestick','Knife','Lead Pipe','Revolver','Rope','Wrench']

# String list of room names
# The way that the list is stylized resembles the actual
# board setup. The number of rooms must be a result of a
# number that is raised to a factor of 2 (a square).
ROOMS = [	'Study', 'Hall', 'Lounge',
			'Library', 'Billiard Room', 'Dining Room',
			'Conservatory','Ballroom','Kitchen'
		]
# List of tuples that represent the secret passages the player can take
# A passage cannot be occupied by a player. ie. the Player shall not
# have a location state of a "secret passage", rather the Player
# "warped" to the connecting room. Secret passages are bi-directional.
# A player may start at elem[0] and end in elem[1] and vice-versa.
SECRET_PASSAGES = [("Study","Kitchen"),("Lounge","Conservatory")]

# Cards are comprised of all suspects, weapons and rooms.
CARDS = SUSPECTS + ROOMS + WEAPONS
