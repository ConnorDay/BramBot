from Player.Player import Player

class Vampire(Player):
    def __init__(self, user, id) -> None:
        super().__init__(user, id)
        self.is_vampire = True