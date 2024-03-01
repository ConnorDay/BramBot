from View import View
import discord

class Narrator(View):
    def __init__(self, first_card, second_card, charmed=False, game=None):
        super().__init__(game=game)
        self.first_card = first_card
        self.second_card = second_card
        self.charmed = charmed

    @discord.ui.button(custom_id="submit", label="Submit", row=2, disabled=True)
    async def submit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        select = discord.utils.find(lambda c: c.custom_id == "count_select", self.children)
        select.disabled = True
        button.disabled = True
        await interaction.response.edit_message(content="Sent response.", view=self)
        if select.values[0] == "First":
            played_card = self.first_card
            discarded = self.second_card
        else:
            played_card = self.second_card
            discarded = self.first_card

        await self.game.NarratorResponse( played_card=played_card, discarded=discarded)

    @discord.ui.select(custom_id="count_select", placeholder="Select Card", row=1, min_values=1, max_values=1, options=[
        discord.SelectOption(label="First"),
        discord.SelectOption(label="Second"),
    ])
    async def player_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        select.placeholder = select.values[0]
        
        button = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
        if not (self.charmed and select.values[0] == "Second"):
            button.disabled = False
        else:
            button.disabled = True
        await interaction.response.edit_message(view=self)
    