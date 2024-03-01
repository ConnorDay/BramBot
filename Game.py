import random
import discord
from Player.Dracula import Dracula
from Player.Player import Player
from Player.Renfield import Renfield
from Player.Vampire import Vampire
from Deck import Deck
from Card.Card import Card
from ModeratorViews.Moderator import Moderator
from PlayerViews.Manipulate import Manipulate
from PlayerViews.Narrator import Narrator

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

    async def Stop(self):
        old_announce = self.announcement_channel

        self.players = []
        self.started = False
        self.moderator = None
        self.deck = Deck()
        self.announcement_channel = None

        self.charm_next_human = False
        self.has_charm = True

        await old_announce.send("Game stopped.")


    async def Author(self, player_id: int):
        player: Player = discord.utils.find( lambda p: p.id == player_id, self.players)

        top_card = self.deck.draw[0]
        await player.send(f"You have been selected as an Author!\nThis is the top card: [{player.parseCardAsAuthor(top_card)}]")
        
        await self.promptModerator()

    async def Narrator(self, player_id: int, is_blind):
        player: Player = discord.utils.find( lambda p: p.id == player_id, self.players)

        first_card = self.deck.draw[0]
        first_card_string = player.parseCardAsNarrator( first_card, is_blind=is_blind )
        second_card = self.deck.draw[1]
        second_card_string = player.parseCardAsNarrator(second_card, is_blind=is_blind)

        charmed=False
        if self.charm_next_human:
            charmed=True
            if player.is_vampire:
                charmed=False
                if player.is_dracula:
                    self.charm_next_human = False
                    self.has_charm = True

        await player.send(f"You have been selected as the Narrator!\nThis is the first card (what the Author saw):\n\n[{first_card_string}]\n\nThis is the second card (no one has seen this):\n\n[{second_card_string}]\n\n\n{'You are Charmed! you must choose the first card.' if charmed else 'Choose which card to play!'}", view=Narrator(first_card, second_card, charmed=charmed, game=self))

    async def NarratorResponse(self, played_card=None, discarded=None):
        assert played_card is not None
        assert discarded is not None

        self.deck.draw.remove(played_card)
        self.deck.draw.remove(discarded)
        self.deck.discard.append(discarded)

        await self.announcement_channel.send(f"The following card was played!\n\n[{str(played_card)}]\n\n\nThere are {len(self.deck.draw)} cards left in the deck.")
        if not played_card.is_ethereal and not played_card.is_rats:
            self.deck.discard.append(played_card)
        
        if played_card.is_rats:
            index = random.randint(0, len(self.deck.draw) - 1)
            self.deck.draw.insert(index, played_card)

        if len(self.deck.draw) < 3:
            self.deck.shuffle()
            await self.announcement_channel.send("The deck has been shuffled.")

        await self.promptModerator()

    async def Manipulate(self, amount: int):
        dracula = discord.utils.find( lambda p: p.is_dracula, self.players )
        for index in range(amount):
            card = self.deck.draw[index]
            await dracula.send(f"You are manipulating the deck. You see the following card {'first' if index == 0 else 'second'}:\n\n[{card}]\n\n\n`Keep`, `bury`, or `Charm!`?", view=Manipulate(card, game=self))
    
    async def ManipulateResponse(self, action: str, card):
        if action == "Keep":
            await self.moderator.send(f"Dracula kept the card!")
        elif action == "Bury":
            self.deck.draw.remove(card)
            self.deck.draw.append(card)
            await self.moderator.send(f"Dracula buried the card!")
        elif action == "Charm!":
            self.has_charm = False
            self.charm_next_human = True
            await self.moderator.send(f"Dracula Charmed! the card!")

        await self.promptModerator()
    
    async def Bite(self, player_id: int):
        player: Player = discord.utils.find( lambda p: p.id == player_id, self.players)
        self.players.remove(player)

        self.players.insert(player.id - 1, Vampire(player.user, player.id))

        await self.promptModerator()

    async def Cure(self, player_id: int):
        player: Player = discord.utils.find( lambda p: p.id == player_id, self.players)
        if player.is_vampire and not player.is_dracula:
            self.players.remove(player)
            self.players.insert(player.id - 1, Player(player.user, player.id))

            await self.announcement_channel.send(f"{player.user.display_name} was successfully Cured!")
        else:
            await self.announcement_channel.send(f"{player.user.display_name} was not Cured!")

        await self.promptModerator()
    
    async def AddCard(self, type: str):
        if type == "Bite!":
            bite = Card(True)
            bite.is_bite = True
            bite.is_ethereal = True
            index = random.randint(1, len(self.deck.draw)-1)
            self.deck.draw.insert(index, bite)
        elif type == "Cure!":
            cure = Card(True)
            cure.is_cure = True
            cure.is_ethereal = True
            index = random.randint(1, len(self.deck.draw)-1)
            self.deck.draw.insert(index, cure)
        else:
            bitc = Card(True)
            bitc.bane = "*Break in the Clouds* Destroy this card after it's played."
            bitc.is_ethereal = True
            index = random.randint(0, len(self.deck.draw)-1)
            self.deck.draw.insert(index, bitc)

        await self.promptModerator()

