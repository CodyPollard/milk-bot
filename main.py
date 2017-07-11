import discord, secrets
from discord.ext.commands import Bot

my_bot = Bot(command_prefix="!")

@my_bot.event
async def on_ready():
    print("Client logged in")

@my_bot.command()
async def hello(*args):
    return await my_bot.say("Hello, world!")

my_bot.run(secrets.token_id)