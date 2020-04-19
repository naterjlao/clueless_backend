#!/usr/bin/python3
from Server import Game

game = Game()

class Resource:

    def main():

        game.add_player("1")
        game.select_character("1", "Miss Scarlet")
        game.add_player("2")
        game.select_character("2", "Mrs White")

        game.start_game()
        game.make_move("1", "Miss Scarlet", "hall-lounge Passage")
        game.end_turn("1")


    '''
        game.add_player("3")
        game.select_suspect("3", "Mrs Peacock")
        game.add_player("4")
        game.select_suspect("4", "Colonel Mustard")
        game.add_player("5")
        game.select_suspect("5", "Mr Green")
        game.add_player("6")
        game.select_suspect("6", "Mrs White")
'''


        #game.make_move("Tolly", "Professor Plum", "study-library Passage")
        #game.end_turn("Tolly")



    main()

