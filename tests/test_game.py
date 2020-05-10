#!/usr/bin/python3
# Functional Regression test for cards
import sys
sys.path.append('..')

from testing_utils import *
from cards import *
from game import *
from gameboard import *
from globals import *
from players import *
from utils import *


g = Game()

g.addPlayer("Bob")
g.addPlayer("Nancy")
g.addPlayer("Rose")
g.addPlayer("Carl")
g.addPlayer("Luke")

g.selectSuspect("Bob","Colonel Mustard")
g.selectSuspect("Nancy","Miss Scarlet")
g.selectSuspect("Rose","Professor Plum")
g.selectSuspect("Carl","Mr Green")

g.startGame() # Cannot start game, luke did not select a character
cycle(g)

g.selectSuspect("Luke","Mrs Peacock")

g.startGame() # Can start a game
cycle(g)
print(g)

g.selectMove('Nancy','Hall-Lounge')
cycle(g)
g.selectMove('Nancy','Hall') # cannot move

g.selectMove('Bob','Dining Room-Lounge')
cycle(g)

g.selectMove('Carl','Ballroom-Conservatory')
cycle(g)

g.selectMove('Luke','Conservatory-Library')
cycle(g)

g.selectMove('Rose','Library-Study')
cycle(g)

print(g)

g.selectMove('Nancy','Hall')
cycle(g)
print(g)

g.proposeSuggestion('Nancy','Mr Green','Lead Pipe')
cycle(g)
print(g)

g.disproveSuggestion('Carl',None,None,True)

