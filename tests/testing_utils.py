# this is not a test

def assertTrue(someBool):
	if someBool:
		print("PASSED")
	else:
		print("FAILED")
		
def assertFalse(someBool):
	assertTrue(not someBool)

def cycle(g,label=""):
	print("---------------------------> CYCLE %s <---------------------------" % str(label))
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
	print("-------------------------> END CYCLE %s <-------------------------" % str(label))