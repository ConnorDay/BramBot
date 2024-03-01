import discord
import re
from ModeratorViews.Command import Command

class Bite(Command):
    def __init__(self, *, game = None):
        super().__init__("Please select someone to Bite!", game=game)

        players = discord.utils.find(lambda c: c.custom_id == "player_select", self.children)
        players.options = self.getPlayersAsOptions()
    
    @discord.ui.button(custom_id="submit", label="Submit", row=2, disabled=True)
    async def submit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        select = discord.utils.find(lambda c: c.custom_id == "player_select", self.children)
        player_id = re.match(r"\d+", select.values[0])[0]
        await interaction.response.send_message("sent message.")
        await self.game.Bite( int(player_id) )

    @discord.ui.select(custom_id="player_select", placeholder="Select Player", row=1, min_values=1, max_values=1, options=[])
    async def player_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        select.placeholder = select.values[0]
        button = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
        button.disabled = False
        await interaction.response.edit_message(view=self)
    