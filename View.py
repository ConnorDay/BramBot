import discord

class View(discord.ui.View):
    def __init__(self, *, game = None):
        super().__init__(timeout=None)

        if game == None:
            raise TypeError("Missing required positional argument 'game'")
        self.game = game

    def remove_custom_items(self):
        for item in self.to_remove:
            self.remove_item(item)

    def getPlayersAsOptions(self):
        options = []
        for player in self.game.players:
            options.append(
                discord.SelectOption(label=f"{player.id}. {player.user.display_name}")
            )

        return options