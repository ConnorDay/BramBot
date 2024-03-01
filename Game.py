import random
import discord
from Player.Dracula import Dracula
from Player.Player import Player
from Player.Renfield import Renfield
from Player.Vampire import Vampire
from Deck import Deck
from ModeratorViews.Moderator import Moderator
from PlayerViews.Manipulate import Manipulate

class Game:
    def __init__(self):
        self.players = []
        self.started = False
        self.moderator = None
        self.deck = Deck()
        self.announcement_channel = None

        self.charm_next_human = False
        self.has_charm = True

    async def addPlayer( self, player ):
        if self.started:
            raise Exception("Added player to already started game")
        self.players.append( Player(player, len(self.players) + 1) )
        await player.send(f"Hello {player.display_name}. You are player number {len(self.players)}")

    async def promptModerator(self):
        lines = ["Cards remaining in deck:", "```"]
        for index, card in enumerate(self.deck.draw):
            lines.append(f"{index+1}. {card}")
        lines.append("```\n")

        lines.append("Players:```")
        for index, player in enumerate(self.players):
            line = f"{index+1}. {player.user.display_name}"

            if player.is_dracula:
                line += " (Dracula)"
            elif player.is_vampire:
                line += " (vampire)"
            elif not player.is_hero:
                line += " (Renfield)"

            lines.append(line)
        lines.append("```\n\n")
        lines.append("Please select a command:")
        await self.moderator.send("\n".join(lines), view=Moderator(game=self))

    async def start( self, moderator, announcement):
        self.moderator = moderator
        self.announcement_channel = announcement

        old_dracula = random.choice(self.players)
        dracula_index = self.players.index(old_dracula)
        self.players.remove(old_dracula)
        dracula = Dracula(old_dracula.user, old_dracula.id)

        old_renfield = random.choice(self.players)
        renfield_index = self.players.index(old_renfield)
        self.players.remove(old_renfield)
        renfield = Renfield(old_renfield.user, old_renfield.id)

        self.players.insert(renfield_index, renfield)
        self.players.insert(dracula_index, dracula)

        lines = [
            "You are the moderator",
            "Here are the players:"
        ]

        for index, player in enumerate(self.players):
            line = f"{index}. {player.user.display_name}"
            if player == dracula:
                line += " (dracula)"
            elif player == renfield:
                line += " (renfield)"
            
            lines.append(line)

        self.started = True
        await self.moderator.send("\n".join(lines))

        await dracula.send(f"You are Dracula!\nRenfield is {renfield.user.display_name} (Player {renfield.id})")
        await renfield.send(f"You are Renfield!\nDracula is {dracula.user.display_name} (Player {dracula.id})")

        self.deck.create()

        await self.promptModerator()

    async def Author(self, player_id: int):
        player: Player = discord.utils.find( lambda p: p.id == player_id, self.players)

        top_card = self.deck.draw[0]
        await player.send(f"You have been selected as an Author!\nThis is the top card: [{player.parseCardAsAuthor(top_card)}]")

    async def Manipulate(self, amount: int):
        dracula = discord.utils.find( lambda p: p.is_dracula, self.players )
        for index in range(amount):
            card = self.deck.draw[0]
            await dracula.send(f"You are manipulating the deck. You see the following card {'first' if index == 0 else 'second'}:\n\n[{card}]\n\n\n`Keep`, `bury`, or `Charm!`?", view=Manipulate(index, game=self))
    
    async def ManipulateResponse(self, action: str, index: int):
        if action == "Keep":
            await self.moderator.send(f"Dracula kept the {'first' if index == 0 else 'second'} card!")
        elif action == "Bury":
            card = self.deck.draw.pop(index)
            self.deck.draw.append(card)
            await self.moderator.send(f"Dracula buried the {'first' if index == 0 else 'second'} card!")
        elif action == "Charm!":
            self.has_charm = False
            self.charm_next_human = True
            await self.moderator.send(f"Dracula Charmed! the {'first' if index == 0 else 'second'} card!")

        await self.promptModerator()