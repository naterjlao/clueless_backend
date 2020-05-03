#!/usr/bin/python3
# Validates the Gameboard class
import sys
sys.path.append('..')

from game import Game

g = Game()
def cycle():
	print("---------------------------> CYCLE <---------------------------")
	print("------gamestate------")
	print(g.getGamestate())
	print("------gameboard------")
	print(g.getGameboard())
	print("------player states------")
	print(g.getPlayerstates())
	print("------move options------")
	print(g.getMoveOptions())
	print("------suggestion options------")
	print(g.getSuggestionOptions())
	print("------accustation options------")
	print(g.getAccusationOptions())
	print("------checklists------")
	print(g.getChecklists())
	print("------cardlists------")
	print(g.getCardlists())
	print("------messages------")
	print(g.getMessages())
	print("-------------------------> END CYCLE <-------------------------")

cycle()
g.addPlayer("Bob")
g.addPlayer("Nancy")
g.addPlayer("Rose")
g.addPlayer("Carl")

g.selectSuspect("Bob","Colonel Mustard")
g.selectSuspect("Nancy","Miss Scarlet")
g.selectSuspect("Rose","Professor Plum")
g.selectSuspect("Carl","Mr Green")



cycle()
g.startGame()
cycle()
g.selectMove("Nancy","Hall-Lounge")
g.selectMove("Nancy","Hall")
cycle()
g.passTurn("Nancy")
cycle()
print(g)
print(g.cardmanager)
