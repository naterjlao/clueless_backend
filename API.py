#!/usr/bin/python3
from Server import Game

game = Game()

class Resource:

    def main():


        game.add_player("1")
        game.select_character("1", "Miss Scarlet")
        game.add_player("2")
        game.select_character("2", "Mrs White")

        '''
        game.select_character("3", "Colonel Mustard")
        game.add_player("4")
        game.select_character("4", "Mrs Peacock")
  
        '''

        game.start_game()

        print(game.get_weapons_list())
        '''
        game.check_move_options(game.get_suspect_current_space("Miss Scarlet").name)
        game.make_move("1", "Miss Scarlet", "hall-lounge Passage")
        game.end_turn("1")

        game.check_move_options(game.get_suspect_current_space("Mrs White").name)
        game.make_move("2", "Mrs White", "ballroom-kitchen Passage")
        game.end_turn("2")

        game.check_move_options(game.get_suspect_current_space("Miss Scarlet").name)
        game.make_move("1", "Miss Scarlet", "Hall")
        game.make_suggestion("1", "Colonel Mustard", "Wrench", "Hall")
        game.end_turn("1")

        game.make_move("2", "Mrs White", "Ballroom")
        game.make_suggestion("2", "Miss Scarlet", "Wrench", "Ballroom")
        game.end_turn("2")

        #game.end_turn("2")

        #game.make_suggestion("Miss Scarlet", "Colonel Mustard", "Wrench", "Lounge")
        #game.end_turn("1")
        '''





    '''
        game.add_player("3")
        game.select_suspect("3", "Mrs Peacock")
        game.add_player("4")
        game.select_suspect("4", "Colonel Mustard")
        game.add_player("5")
        game.select_suspect("5", "Mr Green")
        game.add_player("6")
        game.select_suspect("6", "Mrs White")
        
       # game.make_move("3", "Colonel Mustard", "lounge-dining Passage")
       # game.end_turn("3")
       
       
        #game.make_move("Tolly", "Professor Plum", "study-library Passage")
        #game.end_turn("Tolly")
        
'''





    main()