from View import View
import discord

class Manipulate(View):
    def __init__(self, index: int, game=None):
        super().__init__(game=game)
        self.index = index

        select = discord.utils.find(lambda c: c.custom_id == "count_select", self.children)


    @discord.ui.button(custom_id="submit", label="Submit", row=2, disabled=True)
    async def submit_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        select = discord.utils.find(lambda c: c.custom_id == "count_select", self.children)
        select.disabled = True
        button.disabled = True
        await interaction.response.edit_message(content="Sent response.", view=self)
        await self.game.ManipulateResponse( select.values[0], self.index )

    @discord.ui.select(custom_id="count_select", placeholder="Select Action", row=1, min_values=1, max_values=1, options=[
        discord.SelectOption(label="Keep"),
        discord.SelectOption(label="Bury"),
        discord.SelectOption(label="Charm!")
    ])
    async def player_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        select.placeholder = select.values[0]
        
        if (self.game.has_charm and select.values[0] == "Charm!") or select.values[0] != "Charm!":
            button = discord.utils.find(lambda c: c.custom_id == "submit", self.children)
            button.disabled = False
        await interaction.response.edit_message(view=self)
    