import discord
from View import View
from ModeratorViews.Author import Author
from ModeratorViews.Manipulate import Manipulate
from ModeratorViews.Narrator import Narrator
from ModeratorViews.Bite import Bite
from ModeratorViews.Cure import Cure
from ModeratorViews.AddCard import AddCard

class Moderator(View):
    def __init__(self, *, game = None):
        super().__init__(game=game)
        self.to_remove = []

    @discord.ui.button(custom_id="submit", label="Select", disabled=True, row=2)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        select: discord.ui.Select = discord.utils.find(lambda i: i.custom_id == "select", self.children)
        command = select.placeholder

        view = None
        if command == "Author":
            view = Author(game=self.game)
        elif command == "Manipulate":
            view = Manipulate(game=self.game)
        elif command == "Narrator":
            view = Narrator(game=self.game)
        elif command == "Bite":
            view = Bite(game=self.game)
        elif command == "Cure":
            view = Cure(game=self.game)
        elif command == "Add Card":
            view = AddCard(game=self.game)
        elif command == "Stop Game":
            await self.game.Stop()

        if view != None:
            await interaction.response.send_message(view.message, view=view)
        else:
            await interaction.response.send_message("Sent Command.")

    @discord.ui.select(custom_id="select", placeholder="Select Command", row=1, min_values=1, max_values=1, options=[
        discord.SelectOption(
            label="Manipulate",
            description="Reveals the top x cards to Dracula. Dracula will be given the chance to Manipulate and Charm!"
        ),
        discord.SelectOption(
            label="Author",
            description="Show the top card of the deck to the selected player."
        ),
        discord.SelectOption(
            label="Narrator",
            description="Reveals the top two cards of the deck to the selected player."
        ),
        discord.SelectOption(
            label="Bite",
            description="Turn the selected player into a Vampire"
        ),
        discord.SelectOption(
            label="Cure",
            description="Turn the selected player into a Human. Will reveal to the chat."
        ),
        discord.SelectOption(
            label="Add Card",
            description="Add a card to the deck"
        ),
        discord.SelectOption(
            label="Stop Game",
            description="Stops the current game for all players."
        ),
    ])
    async def select_callback(self, interaction, select: discord.ui.Select):
        self.remove_custom_items()
        select.placeholder = select.values[0]
        button = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
        button.disabled = False
        await interaction.response.edit_message(view=self)