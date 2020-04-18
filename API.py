from Server import Game

game = Game()

class Resource:

    def main():

        game.add_player("1")
        game.select_suspect("1", "Miss Scarlet")
        game.add_player("2")
        game.select_suspect("2", "Professor Plum")
        game.add_player("3")
        game.select_suspect("3", "Mrs Peacock")
        game.add_player("4")
        game.select_suspect("4", "Colonel Mustard")
        game.add_player("5")
        game.select_suspect("5", "Mr Green")
        game.add_player("6")
        game.select_suspect("6", "Mrs White")


        game.start_game()

        #game.make_move("King", "Mrs White", "ballroom-kitchen Passage")
        #game.end_turn("King")

        #game.make_move("Tolly", "Professor Plum", "study-library Passage")
        #game.end_turn("Tolly")



    main()

