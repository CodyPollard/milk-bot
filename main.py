import discord, secrets, quotes, random
from discord.ext.commands import Bot

my_bot = Bot(command_prefix="!")
q = quotes.quote_list


@my_bot.event
async def on_ready():
    print("Client logged in")

@my_bot.command(pass_context=True)
async def add(ctx, *args):
    msg = ctx.message.content
    auth = ctx.message.author
    q.append(msg)

    try:
        q.append(msg)
        return await my_bot.say('Quote successfuly added.')
    except:
        return await my_bot.say('There was an error.')

@my_bot.command()
async def channels(*args):
    c = my_bot.get_all_channels()
    channels = []
    for i in c:
        channels.append(i.name)
    return await my_bot.say('List of currently available channels: \n{}'.format(channels))

@my_bot.command()
async def quotes(*args):
    return await my_bot.say(random.choice(q))

@my_bot.command()
async def close(*args):
    return await my_bot.close()

@my_bot.command()
async def imgay(*args):
    return await my_bot.say('\nI M G A Y\nM\nG\nA\nY')

async def info(*args):
    return await my_bot.say('\nI M G A Y\nM\nG\nA\nY')



def why():
    my_bot.say("This is a meme")




my_bot.run(secrets.token_id)