import random

class Card:
    banes = []
    boons = []
    required_boons = []
    def __init__(self, is_luck: bool):
        self.bane: str = None
        self.boon: str = None
        self.is_luck = is_luck
        self.is_ethereal = False
        self.is_rats = False

    def applyBane(self):
        self.bane = random.choice(Card.banes)
        Card.banes.remove(self.bane)

    def applyBoon(self):
        if len(self.required_boons) > 0:
            self.boon = random.choice(Card.required_boons)
            Card.required_boons.remove(self.boon)
        else:
            self.boon = random.choice(Card.boons)
            Card.boons.remove(self.boon)

    def __str__(self) -> str:
        result = ""
        if self.is_luck:
            result += "Luck"
        else:
            result += "Curse"
        
        if self.bane != None:
            result += f" Bane: '{self.bane}'"
        elif self.boon != None:
            result += f" Boon: '{self.boon}'"

        if self.is_rats:
            result += " Bane: 'Plague of Rats!'"
        
        return result