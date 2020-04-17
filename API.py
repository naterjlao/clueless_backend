from Server import Game

game = Game()

class Resource:

    def main():

        game.add_player("Tolly")
        game.select_suspect("Tolly", "Professor Plum")
        game.add_player("Claire")
        game.select_suspect("Claire", "Mrs Peacock")
        game.add_player("Andrew")
        game.select_suspect("Andrew", "Colonel Mustard")
        game.add_player("Nate")
        game.select_suspect("Nate", "Mr Green")
        game.add_player("King")
        game.select_suspect("King", "Mrs White")
        game.add_player("Queen")
        game.select_suspect("Queen", "Miss Scarlet")

        game.start_game()

        game.make_move("King", "Mrs White", "ballroom-kitchen Passage")
        game.end_turn("King")

        game.make_move("Tolly", "Professor Plum", "study-library Passage")
        game.end_turn("Tolly")



    main()

