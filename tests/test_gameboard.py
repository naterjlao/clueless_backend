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

#g.selectSuspect("Bob","fdkfjdk")
print(g.getPlayerstates())
g.selectSuspect("Bob","Colonel Mustard")
g.selectSuspect("Nancy","Miss Scarlet")
g.selectSuspect("Rose","Professor Plum")
g.selectSuspect("Carl","Mr. Green")


g.startGame()




print(g)
print(g.getPlayerstates())
print(g.getMoveOptions())


