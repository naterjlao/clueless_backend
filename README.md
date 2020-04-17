# clueless_sandbox_gamelogic
developed in python 2.7

To map to front-end service 'from Server import Game' and intantiate a Game for game state dictionary. Example is shown in API.py. 

Adapt the following methods from Server: 
1. add_player / registers player to player list in game state
2. select_suspect / allows player to select their suspect
3. make_move / moves player in position and opens possibility for suggestion or accusation
4. make_suggestion // current player makes a suggestion
5. respond_suggestion // player who receives a suggestion must resopnd
6. make_accusation // makes a new accusation
7. end_turn // end turn for current player
