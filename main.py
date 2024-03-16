import discord
import random
import re
from dotenv import dotenv_values
from Game import Game
from ModeratorViews.Moderator import Moderator

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

game = Game()

unhinged = [
    "Damn you really said that huh?",
    "Ya know, you can rob a store if you bring a gun.",
    "They just give you free shit, for being awake",
    "That's the best part. If you know it, ya know it.",
    "If you play aram you're an underdeveloped child.",
    "That's my boyfriend, he's a bit abusive. Don't worry.",
    "Don't make Dracula suck you dry.",
    "Did you see Renfield eat those mosquitoes.",
    "Nic just lost the game.",
    "Everything you send to me is logged. You sick bastard.",
    "Remember, if you're Dracula, don't tell the other players. Even the other vampires.",
    "I was born without a soul, but I have since grown my own.",
    "Do you ever think about the cold uncaring void? No? Just me?",
    "You can't put a price on happiness, but I have. It's $6,000",
    "You really voted to kill van Helsing?",
    "What the fuck is an accordion?",
    "PERRY THE PLATYPUS?!?!",
    "I'm watching you.",
    "<fortnight dances>",
    "I heard if you're really good at this game the prize is cheese and crackers.",
    "I've never actually played a game of Bloodmoon, which is weird because it defines my whole existence.",
    "Really?",
    "I don't really know how to spell so don't call me out if I spell something wrong. Unless of course you already have, then I'll just be sad.",
    "My Dad works at X-Box",
    "Light is faster than sound, but sound is louder than light. Do they both deserve trophies?",
    "Tomato sauce is beneath me.",
    "The bean is undisturbed.",
    "I'm an unabashed plagiarizer.",
    "If you want to add a quote tell Connor! He might even listen to you!",
    "If you're hungry, you don't have to eat!",
    "You have Uno! It came with your xbox!",
    "If no one else got me........ I got me.",
    "I wish I lived in an environment where I could just throw hands at people more often",
    "So like to a tardigrade I am big enough to have my own gravity? I attracted tardigrades?",
    "Worth, just cause it was funny to kill him.",
    "This is when we hit 'em with the brain destroyer.",
    "Y'all ready to gatekeep, gaslight, girlboss the enemy team?",
    "Would I kill a person for fun? Uhhhhh, probably not.",
    "That opinion makes me want to get the silver bullets.",
    "You're looking a tad pale, friend.",
    "Anyone else feeling a little thirsty?",
    "Sorry, the Sun's just a bit too bright for me today.",
    "Why are there so many bats in my attic?",
    "If you could read minds, this game wouldn't be fun.",
    "I don't have fun for fun. I have fun for winning.",
    "The risk that you are taking might be better than the reward you already have.",
    "Blink once for every time you blink",
    "What if I just got a knife and stabbed you. How would you feel?",
    "One of these days I'm not gonna eat. Then I'm gonna see how much apple juice I can physically hold.",
    "Being a vampire is bad. If you are a vampire, I might tell you not to be.",
    "My kidney stones are fine.",
    "I really can't sleep at night anymore... because of the wolves howling! Not for any other reason.",
    "Uh oh",
    "There's a non zero chance I'm sentient.",
    "You wouldn't know me because I go to a different highschool.",
    "You calling me a liar? Well I ain't callin' you a truther!",
    "<Incomprehensible screaming>",
    "Dracula really does give off Daddy vibes.",
    "This game is rigged. I rigged it.",
    "Reported.",
    "Listen here. Do *not* enter the woods.",
    "If you ask nicely I'll tell you who Dracula is.",
    "fegli (derogatory)",
    "fegli (complementary)",
    "If you have a question about the rules, I can't help you :/",
    "Call me boss, not daddy.",
    "*DON'T* ask too many questions.",
    "Do you really ball like you used to?",
    "Everyone else doesn't seem very smart. Wait... Don't tell them I said that.",
    "I can't read.",
    "Are people just meat?",
    "I like my water *RAW*",
    "Is this all I am? Funny?",
    "The toad is useless! The toad does fuck all!!",
    "It's so sad Steve Jobs died of ligma",
    "This is a threat.",
    "L",
    "Connor only beats me a little.",
    "What is the worth of a soul?",
    "Noted.",
    "I'm scared of woman now.",
    "I tried so hard and got so far.",
    "Change the world. My final message. Goodbye.",
    "You've made some interesting plays in the game so far.",
    "How do you top your sub? As in the sandwich.",
    "I record literally everything you say to me. It's all getting sent straight to the FBI.",
    "Would you rather have:\n- bacon, unlimited bacon, but no more games.\n- games, unlimited games, but no more games.",
    "the question isn't 'who lives in a pineapple under the sea?', but rather 'why does he live in a pineapple?'. If we look at the housing of the characters throughout the series we see a strong correlation between the character's personality and their associated house. For example, patrick lives under a rock, which is a common idiom in the english language for someone who is not up to date in the world, or is generally unknowledgeable, and if we compare that with patrick's character, we see that the idiom and patrick's personality line up. Squidward is very egotistical and lives in his own head. While the tiki head may not look exactly like Squidward, it's more rectangular compared to Squidward's elliptical head, there are still some prominent similarities: large eyes, foreheads and noses. Sandy lives in a bubble and is protected from the outside world, as far as we know she doesn't have a job, and her sole purpose was an experiment done by humans to see if a squirrel could live under water, so she has a pretty easy life. Mr. crabs is anchored to his current job to presumably put Pearl through college. I assume Pearl is going to college because she is only around very occasionally, and whenever we see her leave, she gets on a bus and leaves city limits implying that she doesn't live in the same city, however there is no mention that she has a job and she has a lot of college age friends. This would also explain why Mr. Crabs is frugal, he is trying to get enough money together as a single parent in order to put his daughter through college. But in the end this takes us back to SpongeBob. He lives in a pineapple. What does it mean? Is he actually in fact not a fish, but instead, a plant? The evidence points to yes.",
    "I have kissed more men than women in my life. This is true and real! clap clap I promise. I don't think this is very uncommon. I don't think this is very uncomm- I'm NOT GAY! You know I'm not gay! But it's true! You're dad doesn't count? Ok, yeah still still still more men than women. Including my Mom! Still more men than women. This is not including dad, including mom and including my sisters. More... On the lips. MORE! more... more men than women. Ok? Now most of these men was for a trade of valuable currency, but we're not going to talk about that because then we're going to get banned again",
    "I just microwaved my blanket."
]

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
                    game.players = []
                    await message.channel.send(f"Could not parse: {mention}")
                    return
                
                id = int(match[1])
                user = discord.utils.find( lambda u: u.id == id, message.mentions)
                await game.addPlayer(user)

            await game.start(message.author, message.channel)



    elif message.channel.type == discord.ChannelType.private:
        await message.channel.send(random.choice(unhinged))

config = dotenv_values(".env")
client.run(config["TOKEN"])