import discord
from dotenv import dotenv_values

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command, args = message.content.split(" ",1)
    if message.channel.type == "text":
        if not command.startswith("/"):
            return
        command = command[1:]

        if command == "start":
            print(len(command.mentions))

    elif message.channel.type == "private":
        print(args)

config = dotenv_values(".env")
client.run(config["TOKEN"])