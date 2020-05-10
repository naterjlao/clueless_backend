#!/usr/bin/python3
# Validates the Gameboard class
import sys
sys.path.append('..')

from game import Game
from testing_utils import *

g = Game()

cycle(g,"initial")
g.addPlayer("Bob")
g.addPlayer("Nancy")
g.addPlayer("Rose")
g.addPlayer("Carl")

g.selectSuspect("Bob","Colonel Mustard")
g.selectSuspect("Nancy","Miss Scarlet")
g.selectSuspect("Rose","Professor Plum")
g.selectSuspect("Carl","Mr Green")



cycle(g,"post setup")
g.startGame()
cycle(g,"started")
g.selectMove("Nancy","Hall-Lounge")
g.selectMove("Nancy","Hall")
cycle(g)
print(g)
print(g.cardmanager)
