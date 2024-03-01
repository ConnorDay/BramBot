import discord
import re
from dotenv import dotenv_values
from Game import Game
from ModeratorViews.Moderator import Moderator

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

game = Game()

@client.event
async def on_ready():
    print(f'logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_split = message.content.split(" ")
    command = message_split[0]
    args = message_split[1:]
    if message.channel.type == discord.ChannelType.text:
        if not command.startswith("/"):
            return
        command = command[1:]
        print(f"found command {command} with args {args}")

        if command == "start":
            if game.started:
                message.channel.send("Game already started")
                return

            for mention in args:
                match = re.match(r"<@!?(\d+)>", mention)
                if not match:
                    message.channel.send(f"Could not parse: {mention}")
                    return
                
                id = int(match[1])
                user = discord.utils.find( lambda u: u.id == id, message.mentions)
                await game.addPlayer(user)

            await game.start(message.author, message.channel)



    elif message.channel.type == discord.ChannelType.private:
        await message.channel.send("fegli")

config = dotenv_values(".env")
client.run(config["TOKEN"])