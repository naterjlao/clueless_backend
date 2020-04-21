
class GameException(Exception):
    pass


class InvalidMove(GameException):

    def __init__(self):
        msg = "Try a different Move"
        super(InvalidMove, self).__init__(msg)


class InvalidTurnStatus(GameException):

    def __init__(self):
        msg = "It's not your turn mate"
        super(InvalidTurnStatus, self).__init__(msg)

class InvalidEndTurn(GameException):
    def __init__(self):
        msg = "You can't end your turn yet, try another action"
        super(InvalidEndTurn, self).__init__(msg)

class InvalidSuspect(GameException):

    def __init__(self):
        msg = "You don't own this suspect"
        super(InvalidSuspect, self).__init__(msg)

class InvalidSuggestion(GameException):

    def __init__(self):
        msg = "Must be in same room"
        super(InvalidSuggestion, self).__init__(msg)
