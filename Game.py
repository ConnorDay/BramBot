import random
from Player.Dracula import Dracula
from Player.Player import Player
from Player.Renfield import Renfield
from Player.Vampire import Vampire
from Deck import Deck

class Game:
    def __init__(self):
        self.players = []
        self.started = False
        self.moderator = None
        self.deck = Deck()

    async def addPlayer( self, player ):
        if self.started:
            raise Exception("Added player to already started game")
        self.players.append( Player(player) )
        await player.send(f"Hello {player.name}. You are player number {len(self.players)}")

    async def start( self, moderator):
        self.moderator = moderator

        old_dracula = random.choice(self.players)
        dracula_index = self.players.index(old_dracula)
        self.players.remove(old_dracula)
        dracula = Dracula(old_dracula.user)

        old_renfield = random.choice(self.players)
        renfield_index = self.players.index(old_renfield)
        self.players.remove(old_renfield)
        renfield = Renfield(old_renfield.user)

        self.players.insert(renfield_index, renfield)
        self.players.insert(dracula_index, dracula)

        lines = [
            "You are the moderator",
            "Here are the players:"
        ]

        for index, player in enumerate(self.players):
            line = f"{index}. {player.user.name}"
            if player == dracula:
                line += " (dracula)"
            elif player == renfield:
                line += " (renfield)"
            
            lines.append(line)

        self.started = True
        await self.moderator.send("\n".join(lines))

        self.deck.create()
