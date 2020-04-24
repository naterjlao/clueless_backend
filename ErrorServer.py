


class GameException(Exception):
    pass


class InvalidTurnList(GameException):

    def __init__(self):
        msg = "It's not your turn mate"
        super(InvalidTurnList, self).__init__(msg)


class InvalidTurnStatus(GameException):

    def __init__(self):
        msg = "Wrong move"
        super(InvalidTurnStatus, self).__init__(msg)


class InvalidSuspect(GameException):

    def __init__(self):
        msg = "You don't own this suspect"
        super(InvalidSuspect, self).__init__(msg)

#    def _validate_current_player_owns_suspect(self, suspect):

# not needed
class InvalidMove(GameException):
    def __init__(self):
        msg = "You can't move there"
        super(InvalidMove, self).__init__(msg)


class InvalidSuggestion(GameException):

    def __init__(self):
        msg = "Must be in same room"
        super(InvalidSuggestion, self).__init__(msg)


class InvalidCard(GameException):
    def __init__(self):
        msg = "You do not own the card"
        super(InvalidCard, self).__init__(msg)


class InvalidEndTurn(GameException):
    def __init__(self):
        msg = "You can't end your turn yet, try another action"
        super(InvalidEndTurn, self).__init__(msg)