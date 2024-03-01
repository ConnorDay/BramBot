from Player.Vampire import Vampire

class Dracula(Vampire):
    def __init__(self, user, id) -> None:
        super().__init__(user, id)
        self.is_dracula = True

    def parseCardAsAuthor(self, card, is_blind=False) -> str:
        message = "Dracula sees all: " + str(card)
        return message