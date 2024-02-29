from Player.Player import Player

class Vampire(Player):
    def __init__(self, user) -> None:
        super().__init__(user)
        self.is_vampire = True