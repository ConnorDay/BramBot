from ModeratorViews.Command import Command
import discord
import re

class BlindButton(discord.ui.Select['Narrator']):
    def __init__(self, row=None):
        super().__init__(row=row)
        self.custom_id="blind_select"
        self.options= [
            discord.SelectOption(label="Not Blind", default=True),
            discord.SelectOption(label="Blind")
        ]

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

    

class Narrator(Command):
    def __init__(self, game = None):
        super().__init__("Please select a Narrator", game=game)

        self.add_item(BlindButton(row=2))

        players = discord.utils.find(lambda c: c.custom_id == "player_select", self.children)
        players.options = self.getPlayersAsOptions()

    @discord.ui.select(custom_id="player_select", placeholder="Select Player", min_values=1, max_values=1, row=1, options=[])
    async def player_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        select.placeholder = select.values[0]
        submit = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
        submit.disabled = False

        submit_blind = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
        submit_blind.disabled = False
        await interaction.response.edit_message(view=self)

    @discord.ui.button(custom_id="submit", label="Submit", row=3, disabled=True)
    async def submit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        player_select = discord.utils.find(lambda c: c.custom_id == "player_select", self.children)
        player_id = re.match(r"\d+", player_select.values[0])[0]

        blind_select = discord.utils.find(lambda c: c.custom_id == "blind_select", self.children)
        is_blind = False
        if len(blind_select.values) > 0:
            is_blind = blind_select.values[0] == "Blind"

        await interaction.response.send_message("sent message.")
        await self.game.Narrator( int(player_id), is_blind )