from Player.Player import Player

class Vampire(Player):
    def __init__(self, user, id) -> None:
        super().__init__(user, id)
        self.is_vampire = True

    def parseCardAsNarrator(self, card, is_blind=False) -> str:
        if is_blind and not card.is_always_visible:
            if card.is_luck:
                return "Luck"
            return "Curse"
        
        return str(card)