from Player.Player import Player

class Renfield(Player):
    def __init__(self, user):
        super().__init__(user)
        self.is_hero = False 