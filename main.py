from discord.ext.commands import Bot
from Misc import quotes
import random, secrets

my_bot = Bot(command_prefix="!")
q = quotes.quote_list

@my_bot.event
async def on_ready():
    print("Client logged in")
    quotes.update_quotes()

# Meta Commands #

@my_bot.command()
async def info(*args):
    return await my_bot.say('I am currently hosted at: https://github.com/CodyPollard/milk-bot\n'
                            'To suggest features and track development type !ra for access to the bot-help channel.')

@my_bot.command(pass_context=True)
async def ra(ctx, *args):
    r = ctx.message.server.roles
    for i in r:
        if i.name == "Bot Tester":
            return await my_bot.add_roles(ctx.message.author, i)

@my_bot.command()
async def close(*args):
    return await my_bot.close()

@my_bot.command()
async def channels(*args):
    c = my_bot.get_all_channels()
    channels = []
    for i in c:
        channels.append(i.name)
    return await my_bot.say('List of currently available channels: \n{}'.format(channels))

# Quote Commands #

@my_bot.command(pass_context=True)
async def add(ctx, *args):
    msg = ctx.message.content
    auth = ctx.message.author
    try:
        quotes.add_quote(msg)
        return await my_bot.say('Quote successfuly added.')
    except quotes.SanitationError as exception:
        return await my_bot.say(exception)

@my_bot.command()
async def quote(*args):
    return await my_bot.say(random.choice(q))

# Misc Commands #

@my_bot.command()
async def imgay(*args):
    return await my_bot.say('\nI M G A Y\nM\nG\nA\nY')


# Start the bot
my_bot.run(secrets.token_id)