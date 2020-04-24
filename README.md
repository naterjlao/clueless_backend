# clueless_sandbox_gamelogic
developed in python 2.7

To map to front-end service 'from Server import Game' and intantiate a Game for game state dictionary. Example is shown in API.py. 

1. add_player to register player objects to be created upon game_start
2. select_suspect allows the player just added to select their game character
3. start_game creates a gamestate with the players who were added
4. make_move in order to navigate the gameboard
	4a. the Room must be available (Rooms always, Hallways one at a time)
	4b. when character enters Room for the first time they must make a Suggestion with that room as one of the variables
5. make_suggestion - to make a new suggestion after entering a new room
	5a. name - is the name of the player (player 0, player 1)
	5b. suspect - what character are they suspeting (forcibly moved to room)
	5c. room - what room are they suggesting
	5d. weapon - what weapon are they suggesting (forcibly moved to room)
6. respond_suggestion
7. make_accusation - makes a new accusation which allows player to win game if correct or lose and be deleted from turn list if false. 
