import random
from Card.Card import Card

class Deck:
    banes = [
        "Author does **not** view top card next turn",
        "Author and Narrator do **not** see Banes or Boons next turn",
        "Renfield destroys 2 Editor Tokens of their choice",
        "Dracula manipulates the top 2 cards next turn"
    ]
    boons = [
        "Dracula does **not** manipulate the deck next turn",
        "Dracula can**not** Charm! next turn",
    ]

    def __init__(self) -> None:
        self.discard = []

        ethereal = Card(is_luck=False)
        ethereal.boon = "Add a *Break in the Clouds* to the deck"
        ethereal.is_ethereal = True
        self.draw = [ ethereal ]
        self.has_shuffled = False

        self.banes = []
        self.boons = []

    def addBane(self, card: Card):
        self.draw.append(card)
        self.banes.append(card)
    def addBoon(self, card: Card):
        self.draw.append(card)
        self.boons.append(card)

    def create(self):
        Card.banes = Deck.banes.copy()
        Card.boons = Deck.boons.copy()
        for i in range(3):
            self.draw.append(Card(is_luck=False))
            self.draw.append(Card(is_luck=True))

            luck_bane = Card(is_luck=True)
            luck_bane.applyBane()
            self.addBane(luck_bane)

            if i != 0:
                curse_boon = Card(is_luck=False)
                curse_boon.applyBoon()
                self.addBoon(curse_boon)
        
        curse_bane = Card(is_luck=False)
        curse_bane.applyBane()
        self.addBane(curse_bane)

        rats = Card(is_luck=False)
        rats.is_rats = True

        self.draw.append(rats)

        random.shuffle(self.draw)

    def shuffle(self):
        if not self.has_shuffled:
            Card.required_boons.append("Players **vote to choose** next Author, after which Authorship is restored to the player who should have been next.")
            self.has_shuffled = True

        Card.banes = Deck.banes.copy()
        for card in self.banes:
            card.applyBane()

        Card.boons = Deck.boons.copy()
        for card in self.boons:
            card.applyBoon()
        
        self.draw.extend(self.discard)
        self.discard = []
        random.shuffle(self.draw)