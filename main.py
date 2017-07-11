import discord, secrets, quotes, random
from discord.ext.commands import Bot

my_bot = Bot(command_prefix="!")
q = quotes.quote_list


@my_bot.event
async def on_ready():
    print("Client logged in")


@my_bot.command()
async def anime(*args):
    return await my_bot.say("kys")

@my_bot.command()
async def testing(*args):
    c = my_bot.get_all_channels()
    for i in c:
        return await my_bot.say(i.name)

@my_bot.command()
async def quotes(*args):
    return await my_bot.say(random.choice(q))



my_bot.run(secrets.token_id)
# print(private_channels)