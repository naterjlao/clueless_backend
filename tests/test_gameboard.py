#!/usr/bin/python3
# Validates the Gameboard class
import sys
sys.path.append('..')

from game import Game

g = Game()
g.addPlayer("Bob")
g.addPlayer("Nancy")
g.addPlayer("Rose")
g.addPlayer("Carl")

g.selectSuspect("Bob","Colonel Mustard")
g.selectSuspect("Nancy","Miss Scarlet")
g.selectSuspect("Rose","Professor Plum")
g.selectSuspect("Carl","Mr Green")

def cycle():
	print("---------------------------> CYCLE <---------------------------")
	print(g.getGamestate())
	print(g.getGameboard())
	print(g.getPlayerstates())
	print(g.getMoveOptions())
	print(g.getSuggestionOptions())
	print(g.getAccusationOptions())
	print(g.getChecklists())
	print(g.getMessages())

cycle()
g.startGame()
cycle()
g.selectMove("Bob","Ballroom-Conservatory")
cycle()
print(g)
