from ModeratorViews.Command import Command
import discord
import re

class Manipulate(Command):
    def __init__(self, *, game=None):
        super().__init__("Please select a number of cards to manipulate", game=game)
        
    @discord.ui.button(custom_id="submit", label="Submit", row=2)
    async def submit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        select = discord.utils.find(lambda c: c.custom_id == "count_select", self.children)
        
        amount = 1
        if len(select.values) > 0:
            amount = re.match(r"\d+", select.values[0])[0]
        await interaction.response.send_message("sent message.")
        await self.game.Manipulate( int(amount) )

    @discord.ui.select(custom_id="count_select", placeholder="1", row=1, min_values=1, max_values=1, options=[
        discord.SelectOption(label="1"),
        discord.SelectOption(label="2")
    ])
    async def player_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        select.placeholder = select.values[0]
        button = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
        button.disabled = False
        await interaction.response.edit_message(view=self)
    