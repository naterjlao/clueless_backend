import unittest
import Entity



class Test(unittest.TestCase):

    def test_format_card(self):
        game_card = Entity.Card(
            item = Entity.WRENCH, item_type = Entity.WEAPON)
        card_dict = game_card.format()
        self.assertEqual(game_card.item, card_dict["item"])
        self.assertEqual(game_card.type, card_dict["item_type"])


class TestSuggestion(unittest.TestCase):

    def test_format_suggestion(self):
        pass


class TestPlayer(unittest.TestCase):

    def test_format_player(self):
        pass

class TestPassage(unittest.TestCase):

    def test_create_passage(self):
        pass

    def test_format_passage(self):
        pass

class TestRooms(unittest.TestCase):

    def test_create_room(self):
        pass

    def test_format_room(self):
        pass

class TestHomeSquare(unittest.TestCase):

    def test_create_homesquare(self):
        pass

    def test_format_homesquare(self):
        pass


class TestGameModel(unittest.TestCase):

    def gamemodel_start_test(self):
        pass

    def gamemodel_format_test(self):
        pass



class TestGameModelBuilder(unittest.TestCase):

    def gamebuilder_start_test(self):
        self.players = [
            Entity.Player(user = "test1", suspect = Entity.PLUM),
            Entity.Player (user = "test2", suspect = Entity.MUSTARD)]






