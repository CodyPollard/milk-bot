from discord.ext.commands import Bot
from misc import misc, quotes
import random, secrets, time

milk_bot = Bot(command_prefix="!")
quoteList = quotes.quote_list
eight = misc.eightball

@milk_bot.event
async def on_ready():
    print("Client logged in")
    quotes.update_quotes()

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

@milk_bot.command()
async def templink(*args):
    """Displays a join link for the Discord server"""
    return await milk_bot.say("Temp link: https://discord.gg/5tnDXvZ")

# Quote Commands #

@milk_bot.command(pass_context=True)
async def add(ctx, *args):
    """Adds the message content to quotes.txt if formatted correctly"""
    msg = ctx.message.content
    try:
        quotes.add_quote(msg)
        return await milk_bot.say('Quote successfully added.')
    except quotes.ValidationError as exception:
        return await milk_bot.say(exception)

@milk_bot.command()
async def quote(*args):
    """Displays a random quote from quotes.txt"""
    return await milk_bot.say(random.choice(quoteList))

# Other Commands #

@milk_bot.command()
async def imgay(*args):
    """First rule of Fight Club"""
    return await milk_bot.say('\nI  M  G  A  Y\nM\nG\nA\nY')

@milk_bot.command(name='8ball')
async def eightball(*args):
    """Ask it a question"""
    return await milk_bot.say(random.choice(eight))

# Start the bot
milk_bot.run(secrets.token_id)
