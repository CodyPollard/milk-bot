from discord.ext.commands import Bot
from misc import misc, quotes, user_metrics, sqlite_quotes
from settings import Settings, PROGRAM_PATH
import random, secrets, os, logging
from pymongo import MongoClient
from discord.ext.commands.errors import BadArgument

# DB info
client = MongoClient()
db = client.coc
# Settings
settings = Settings()
admins = settings.admins
# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler(PROGRAM_PATH + '/main.log')
handler.setLevel(logging.DEBUG)
# Logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# Misc
milk_bot = Bot(command_prefix="!")
eight = misc.eightball


# Runs on startup
@milk_bot.event
async def on_ready():
    logger.info('Client logged in.')
    logger.debug('Starting cycles.')


# Statup stuff #
# def get_all_chaos_players():
#     all_chaos_players = []
#     for i in db.players.find():
#         all_chaos_players.append(i['name'].split('#')[0].lower().split(' ')[0])
#     return all_chaos_players


# Meta Commands #

@milk_bot.command()
async def info(*args):
    """Displays info about the bot's code and the !ra command"""
    return await milk_bot.say('I am currently hosted at: https://github.com/CodyPollard/milk-bot\n'
                              'To suggest features and track development type !ra for access to the bot-help channel.')


@milk_bot.command(pass_context=True)
async def settings(ctx, *args):
    """Allows admins to adjust some variable bot settings'"""
    # Check for admin role or something here
    s = Settings()
    msg = ctx.message.content
    tmpset = Settings()
    if s.is_admin(str(ctx.message.author)):
        if msg == '!settings':
            # Display list of changeable settings
            return await milk_bot.say('To change a setting use !settings [command] [value]\n'
                                      'Available settings include:\n'
                                      'interval - Set quote interval by the hour.')
            pass
        elif msg.split(' ')[1] == 'interval':
            # Validate and set quote interval
            # Cast third portion of command as an int for validation
            interval = int(msg.split(' ')[2])
            if tmpset.validate_quote_interval(interval) is True:
                tmpset.set_quote_interval(interval)
                return await milk_bot.say('Quote interval set to {} hours'.format(interval))
            else:
                return await milk_bot.say('Please enter a valid interval between 1 and 12')
        else:
            return await milk_bot.say("That command doesn't exist. Use !settings to get a list of valid commands")
    else:
        return await milk_bot.say('You do not have access to this command.')


# Quote Commands #

@milk_bot.command(pass_context=True)
async def add(ctx, *args):
    """
    Adds the message content to the quotes db
    !add "[quote]" -[author]
    """
    msg = ctx.message.content
    author = ctx.message.author
    p = user_metrics.UserProfile(author)
    try:
        if p.user_exists():
            # quotes.validate_quote(msg)
            p.increment_add()
            sqlite_quotes.validate_quote(msg, p.usr)
            return await milk_bot.say('Quote successfully added.')
        else:
            return await milk_bot.say('Please create a profile using !newprofile to gain access to this command.')
    except sqlite_quotes.ValidationError as exception:
        return await milk_bot.say(exception)


@milk_bot.command(pass_context=True)
async def quote(ctx, *args):
    """Displays a random quote from quotes.txt"""
    author = ctx.message.author
    p = user_metrics.UserProfile(author)
    if p.user_exists():
        p.increment_quote()
        q = sqlite_quotes.get_random_quote()
        return await milk_bot.say('"{}" - {}'.format(q[0][0], q[0][-1]))
    else:
        return await milk_bot.say('Please create a profile using !newprofile to gain access to this command.')


# Other Commands #

@milk_bot.command(pass_context=True, name='8ball')
async def eightball(ctx, *args):
    """Ask it a question"""
    author = ctx.message.author
    p = user_metrics.UserProfile(author)
    if p.user_exists():
        p.increment_eightball()
        return await milk_bot.say(random.choice(eight))
    else:
        return await milk_bot.say('Please create a profile using !newprofile to gain access to this command.')


@milk_bot.command(pass_context=True)
async def slist(ctx, *args):
    """
    Shopping list for logistics trips to empire
    !slist - Displays the full shopping list
    !slist [item] - Adds given item to the list
    !slist clear - Clears the shopping list
    """
    msg = ctx.message.content
    if msg == '!slist':
        s = ''
        try:
            with open('shoppinglist.txt', 'r') as f:
                temp = f.read().splitlines()
                for i in temp:
                    s +=(i+'\n')
            return await milk_bot.say(s)
        except FileNotFoundError:
            return await milk_bot.say('File does not exist. Use !slist [item] to add to a new list.')
    elif msg.split(' ')[1] == 'clear':
        os.remove('shoppinglist.txt')
        return await milk_bot.say('Shopping list cleared.')
    else:
        n = msg.split(' ', 1)[1]
        misc.write_shopping_list(n)
        return await milk_bot.say('Succesfully added {} to the shopping list.\n'
                                  'Use !slist to view full list'.format(n))


# Metric Commands #

@milk_bot.command(pass_context=True)
async def newmetrics(ctx, *args):
    s = Settings()
    if s.is_admin(str(ctx.message.author)):
        user_metrics.initialize_user_metrics_db()
        return await milk_bot.say("Initialized")
    else:
        return await milk_bot.say('You do not have access to this command.')


@milk_bot.command(pass_context=True)
async def newquotes(ctx, *args):
    s = Settings()
    if s.is_admin(str(ctx.message.author)):
        sqlite_quotes.initialize_quote_db()
        return await milk_bot.say("Initialized")
    else:
        return await milk_bot.say('You do not have access to this command.')


@milk_bot.command(pass_context=True)
async def readmetrics(ctx, *args):
    # user_metrics.read_db()
    s = Settings()
    if s.is_admin(str(ctx.message.author)):
        return await milk_bot.say(user_metrics.read_db())
    else:
        return await milk_bot.say('You do not have access to this command.')


@milk_bot.command(pass_context=True)
async def readquotes(ctx, *args):
    # user_metrics.read_db()
    s = Settings()
    if s.is_admin(str(ctx.message.author)):
        return await milk_bot.say(sqlite_quotes.read_db())
    else:
        return await milk_bot.say('You do not have access to this command.')


@milk_bot.command(pass_context=True)
async def newprofile(ctx, *args):
    author = ctx.message.author
    p = user_metrics.UserProfile(author)
    # user_metrics.read_db()
    response = p.create_profile()
    return await milk_bot.say(response)


@milk_bot.command(pass_context=True)
async def injectprofile(ctx, *args):
    s = Settings()
    author = ctx.message.author
    msg = ctx.message.content.split(' ')
    if s.is_admin(str(ctx.message.author)):
        if msg[-1] == '!injectprofile':
            return await milk_bot.say('Please provide a profile to create.')
        else:
            p = user_metrics.UserProfile(author)
            response = p.inject_profile(msg[-1])
            return await milk_bot.say(response)
    else:
        return await milk_bot.say('You do not have access to this command.')


@milk_bot.command(pass_context=True)
async def profile(ctx, *args):
    author = ctx.message.author
    msg = ctx.message.content
    p = user_metrics.UserProfile(author)
    if '!profile' in msg.split(' ')[-1]:
        if p.user_exists():
            # Stat order (quote, eightball, add, alias)
            stats = p.get_profile()
            return await milk_bot.say('```Stats for {}\nQuotes: {}\n8Ball: {}\nAdd: {}\nAlias: {}```'
                                      .format(p.usr, stats[0], stats[1], stats[2], stats[3]))
        else:
            return await milk_bot.say('Please create a profile using !newprofile to access this command.')
    elif 'addalias' in msg.split(' ')[1]:
        return await milk_bot.say(p.add_alias(msg.split(' ')[-1]))
    else:
        return await milk_bot.say('Invalid command.')


# Start the bot
milk_bot.run(secrets.token_id)
