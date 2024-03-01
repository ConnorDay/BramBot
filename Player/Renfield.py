from Player.Player import Player

class Renfield(Player):
    def __init__(self, user, id):
        super().__init__(user, id)
        self.is_hero = False 