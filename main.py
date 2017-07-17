from discord.ext.commands import Bot
from misc import misc
import random, secrets

milk_bot = Bot(command_prefix="!")
quoteList = misc.quote_list
eight = misc.eightball

@milk_bot.event
async def on_ready():
    print("Client logged in")
    misc.update_quotes()

# Meta Commands #

@milk_bot.command()
async def info(*args):
    """Displays info about the bot's code and the !ra command"""
    return await milk_bot.say('I am currently hosted at: https://github.com/CodyPollard/milk-bot\n'
                            'To suggest features and track development type !ra for access to the bot-help channel.')

@milk_bot.command(pass_context=True)
async def ra(ctx, *args):
    """Grants user the role 'Bot Tester'"""
    r = ctx.message.server.roles
    for i in r:
        if i.name == "Bot Tester":
            return await milk_bot.add_roles(ctx.message.author, i)

# Quote Commands #

@milk_bot.command(pass_context=True)
async def add(ctx, *args):
    """Adds the message content to quotes.txt if formated correctly"""
    msg = ctx.message.content
    try:
        misc.add_quote(msg)
        return await milk_bot.say('Quote successfuly added.')
    except misc.ValidationError as exception:
        return await milk_bot.say(exception)

@milk_bot.command()
async def quote(*args):
    """Displays a random quote from quotes.txt"""
    return await milk_bot.say(random.choice(quoteList))

# Other Commands #

@milk_bot.command()
async def imgay(*args):
    """First rule of fight club"""
    return await milk_bot.say('\nI M G A Y\nM\nG\nA\nY')

@milk_bot.command(name='8ball')
async def eightball(*args):
    """Standard 8-ball"""
    return await milk_bot.say(random.choice(eight))

# Start the bot
milk_bot.run(secrets.token_id)