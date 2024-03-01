from ModeratorViews.Command import Command
import discord
import re

class AddCard(Command):
    def __init__(self, *, game=None):
        super().__init__("Please select a card to add", game=game)
        
    @discord.ui.button(custom_id="submit", label="Submit", row=2)
    async def submit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        select = discord.utils.find(lambda c: c.custom_id == "count_select", self.children)
        
        await interaction.response.send_message("sent message.")
        await self.game.AddCard( select.values[0] )

    @discord.ui.select(custom_id="count_select", placeholder="Select a card", row=1, min_values=1, max_values=1, options=[
        discord.SelectOption(label="Break in the Clouds"),
        discord.SelectOption(label="Bite!"),
        discord.SelectOption(label="Cure!")
    ])
    async def player_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        select.placeholder = select.values[0]
        button = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
        button.disabled = False
        await interaction.response.edit_message(view=self)
    