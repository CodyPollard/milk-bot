from discord.ext.commands import Bot
from misc import misc, quotes
from CoC import player
import random, secrets
from pymongo import MongoClient

# DB info
client = MongoClient()
db = client.coc

milk_bot = Bot(command_prefix="!")
eight = misc.eightball

@milk_bot.event
async def on_ready():
    print("Client logged in")


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
    """
    Adds the message content to the quotes db
    !add "[quote]" -[author]
    """
    msg = ctx.message.content
    try:
        quotes.validate_quote(msg)
        return await milk_bot.say('Quote successfuly added.')
    except quotes.ValidationError as exception:
        return await milk_bot.say(exception)

@milk_bot.command(pass_context=True)
async def quote(ctx, *args):
    """Displays a random quote from quotes.txt"""
    try:
        q = quotes.DBQuote()
        msg = ctx.message.content
        call_total = quotes.get_call_count_total()
        if '!quote' in msg.split(' ')[-1]:  # Print a random quote if no author is given
            q.get_quote()
            formatted = '{0:.3g}'.format(q.quote['call_count'] / call_total * 100)
            return await milk_bot.say('"{}"{} \nThis quote has been used {} times accounting for'
                                      ' {}% of total usage.'.format(q.quote['msg'], q.quote['author'], q.quote['call_count'], formatted))
        else:  # Print a random quote by the given author
            q.get_quote(msg.split(' ')[1])
            formatted = '{0:.3g}'.format(q.quote['call_count'] / call_total * 100)
            return await milk_bot.say('"{}"{} \nThis quote has been used {} times accounting for'
                                      ' {}% of total usage.'.format(q.quote['msg'], q.quote['author'], q.quote['call_count'], formatted))
    except quotes.ValidationError as exception:
        return await milk_bot.say(exception)


# Other Commands #

@milk_bot.command(name='8ball')
async def eightball(*args):
    """Ask it a question"""
    return await milk_bot.say(random.choice(eight))



# COC COMMANDS #

@milk_bot.command(pass_context=True)
async def coc(ctx, *args):
    msg = ctx.message.content
    user = str(ctx.message.author)
    # Runs if !coc newgame is given
    if 'newgame' in msg.split(' ')[-1]:
        # Check to see if the user already has a profile
        if db.players.find({'name': user}).count() is 0:
            pass
        else:
            return await milk_bot.say('Your profile already exists. Type !coc help for more info.')
        # Ask the user to select a race
        await milk_bot.say('Please select a race: Human, Orc, Dwarf, or Nightelf')
        race = await milk_bot.wait_for_message(author=ctx.message.author, timeout=10)
        if race is None:
            return await milk_bot.say('Race selection timed out, please try !coc newgame again when you are ready.')
        player.new_game(user, str(race.content).lower())
        return await milk_bot.say('Your profile has been created, please see !coc help for more info')
    # Runs if !coc delete is given
    elif 'delete' in msg.split(' ')[-1]:
        if db.players.find({'name': user}).count() is 0:
            return await milk_bot.say('Your profile does not exist. Type !coc newgame to create one.')
        else:
            await milk_bot.say('Are you sure you want to delete your profile? y/n')
            confirmation = await milk_bot.wait_for_message(author=ctx.message.author, timeout=20)
            if str(confirmation.content).lower() == 'y':
                db.players.delete_one({'name': user})
                return await milk_bot.say('Profile deleted.')
            else:
                return await milk_bot.say('You live to fight another day.')
    # Runs if !coc myinfo is given
    elif 'myinfo' in msg.split(' ')[-1]:
        if db.players.find({'name': user}).count() is 0:
            return await milk_bot.say('Your profile does not exist. Type !coc newgame to create one.')
        else:
            p = player.Player(user)
            return await milk_bot.send_message(ctx.message.author, p.get_stats())
    # Runs if !coc help is given
    elif 'help' in msg.split(' ')[-1]:
        return await milk_bot.say('Valid commands include: \n'
                                    "newgame : Creates a new profile if you don't have one already.\n"
                                    'delete : Deletes your profile if one exists.\n'
                                    'myinfo : Sends your current stats in a private message.\n'
                                    'help : Displays this list.')
    # Runs if none of the above commands are given
    else:
        return await milk_bot.say('Invalid command. Please see !coc help for more info')

# Start the bot
milk_bot.run(secrets.token_id)
