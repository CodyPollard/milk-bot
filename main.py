import asyncio, logging
from discord.ext.commands import Bot
from misc import misc, quotes
from CoC import player, coc
from settings import Settings
import random, secrets, os
from pymongo import MongoClient

# DB info
client = MongoClient()
db = client.coc
# Settings
settings = Settings()
admins = settings.admins
quote_interval = settings.quote_interval

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler('main.log')
handler.setLevel(logging.DEBUG)
# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(handler)

# Other stuff
milk_bot = Bot(command_prefix="!")
eight = misc.eightball
CHAOS_PLAYER_NAMES = None


# Runs on startup
@milk_bot.event
async def on_ready():
    logger.info('Client logged in.')
    logger.debug('Starting cycles.')
    global CHAOS_PLAYER_NAMES
    # Start cycles
    coc.recruitment_cycle()
    CHAOS_PLAYER_NAMES = get_all_chaos_players()
    # Load settings
    await hourly_quote()


# Statup stuff #
@milk_bot.event
async def hourly_quote():
    # Definitions
    q = quotes.DBQuote()
    # Sunflower ID 438162774917644288, general ID 438162774917644290, milk-general ID 222412917365145601
    sunflower_general = milk_bot.get_channel('438162774917644290')
    milk_general = milk_bot.get_channel('222412917365145601')
    channel_list = [sunflower_general, milk_general]

    while True:
        # Check if any messages have been sent since last quote
        async for message in milk_bot.logs_from(sunflower_general, limit=1):
            if 'milk-bot' in str(message.author):
                logging.debug('Last message was from milk_bot, skipping quote for this cycle.')
                break
            else:
                logging.debug('Posting quote for this cycle.')
                # Print a quote at the end of the timer
                call_total = quotes.get_call_count_total()
                q.get_quote()
                formatted = '{0:.3g}'.format(q.quote['call_count'] / call_total * 100)
                for i in channel_list:
                    await milk_bot.send_message(i, '"{}"{} \nThis quote has been used {} times accounting for'
                                                                   ' {}% of total usage.'.format(q.quote['msg'],
                                                                                                 q.quote['author'],
                                                                                                 q.quote['call_count'],
                                                                                                 formatted))

        # Sleep event for x hours
        sleep_time = 60*60*quote_interval
        logger.debug('Sleeping for %s seconds.', sleep_time)
        await asyncio.sleep(sleep_time)


def get_all_chaos_players():
    all_chaos_players = []
    for i in db.players.find():
        all_chaos_players.append(i['name'].split('#')[0].lower().split(' ')[0])
    return all_chaos_players


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
    msg = ctx.message.content
    tmpset = Settings()
    if str(ctx.message.author) in admins:
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


# COC COMMANDS #
@milk_bot.command(pass_context=True)
async def chaos(ctx, *args):
    msg = ctx.message.content
    user = str(ctx.message.author)
    # Runs if !chaos newgame is given
    if 'newgame' in msg.split(' ')[-1]:
        # Check to see if the user already has a profile
        if db.players.find({'name': user}).count() > 0:
            return await milk_bot.say('Your profile already exists. Type !chaos help for more info.')
        # Ask the user to select a race
        await milk_bot.say('Please select a race: Human, Orc, Dwarf, or Nightelf')
        race = await milk_bot.wait_for_message(author=ctx.message.author, timeout=10)
        if race is None:
            return await milk_bot.say('Race selection timed out, please try !chaos newgame again when you are ready.')
        elif str(race.content).lower() in ('human', 'orc', 'dwarf', 'nightelf'):
            player.Player(user, str(race.content).lower())
            return await milk_bot.say('Your profile has been created, please see !chaos help for more info')
        else:
            return await milk_bot.say('Your selected race was not one of the four listed above. Please create a newgame'
                                      'to try again.')
    # Runs if !chaos delete is given
    elif 'delete' in msg.split(' ')[-1]:
        if db.players.find({'name': user}).count() is 0:
            return await milk_bot.say('Your profile does not exist. Type !chaos newgame to create one.')
        else:
            await milk_bot.say('Are you sure you want to delete your profile? y/n')
            confirmation = await milk_bot.wait_for_message(author=ctx.message.author, timeout=20)
            if str(confirmation.content).lower() == 'y':
                db.players.delete_one({'name': user})
                db.armies.delete_one({'owner': user})
                db.castles.delete_one({'owner': user})
                return await milk_bot.say('Profile deleted.')
            else:
                return await milk_bot.say('You live to fight another day.')
    # Runs if !chaos help is given
    elif 'help' in msg.split(' ')[-1]:
        return await milk_bot.say("For a full list of commands refer to the Bot's GitHub page.\n"
                                  "https://github.com/CodyPollard/milk-bot")
    # Runs if !chaos top3 is given
    elif 'top3' in msg.split(' ')[-1]:
        leaders = coc.get_top_three()

        out = []
        for i in leaders:
            out.append('{}: {}'.format(i, leaders[i]))
        return await milk_bot.say('Top 3 Leaderboard:\n'
                                  '{}\n'
                                  '{}\n'
                                  '{}'.format(out[0], out[1], out[2]))
    # Runs if none of the above commands are given
    else:
        return await milk_bot.say('Invalid command. Please see !chaos help for more info')


@milk_bot.command(pass_context=True)
async def mystats(ctx, *args):
    msg = ctx.message.content
    user = str(ctx.message.author)
    # Runs if !chaos myinfo is given
    if db.players.find({'name': user}).count() is 0:
        return await milk_bot.say('Your profile does not exist. Type !chaos newgame to create one.')
    elif 'army' in msg.split(' ')[-1]:
        a = player.Army(user)
        return await milk_bot.send_message(ctx.message.author, '- Soldiers -\n'
                                                               'Footmen: {}\n'
                                                               'Spies: {}\n'
                                                               'Sentries: {}\n\n'
                                                               '- Weapons -\n'
                                                               'Short Swords: {}\n'
                                                               'Flails: {}\n'
                                                               'Halberds: {}\n'
                                                               'Cavalry: {}\n-\n'
                                                               'Kite Shields: {}\n'
                                                               'Spears: {}\n'
                                                               'Tower Shields: {}\n'
                                                               'Full Armor: {}\n\n'
                                                               '- Tools -\n'
                                                               'Rope: {}\n'
                                                               'Grappling Hooks: {}\n'
                                                               'Short Bows: {}\n-\n'
                                                               'Torches: {}\n'
                                                               'Guard Dogs: {}\n'
                                                               'Alarms: {}'.format(a.s_footman, a.c_spy, a.c_sentry,
                                                                                   a.ow_short_sword, a.ow_flail, a.ow_halberd, a.ow_cavalry,
                                                                                   a.dw_kite_shield, a.dw_spear, a.dw_tower_shield, a.dw_full_armor,
                                                                                   a.st_rope, a.st_grapple_hook, a.st_short_bow,
                                                                                   a.sen_torch, a.sen_guard_dog, a.sen_alarm))
    elif 'castle' in msg.split(' ')[-1]:
        c = player.Castle(user)
        return await milk_bot.send_message(ctx.message.author, 'Current Upgrade Tier: {}\n'
                                                               'Defense: {}\n'
                                                               'Unit Capacity: {}\n'
                                                               '-----\n'
                                                               'Next Upgrade At: xyz Gold'.format(c.upgrade_tier,
                                                                                                  c.defense, c.capacity))
    else:
        p = player.Player(user)
        return await milk_bot.send_message(ctx.message.author, 'Race: {}\n'
                                                               'Recruitment Rate: {}\n'
                                                               'Gold: {}\n'
                                                               'Attack Power: {}\n'
                                                               'Defense Power: {}\n'
                                                               'Spy Power: {}\n'
                                                               'Sentry Power: {}'.format(p.race, p.recruit_rate, p.gold,
                                                                                         p.attack_power, p.defense_power,
                                                                                         p.spy_power, p.sentry_power))


@milk_bot.command(pass_context=True)
async def raceinfo(ctx, *args):
    msg = ctx.message.content
    user = str(ctx.message.author)
    if 'human' in msg.split(' ')[-1]:
        r = player.Race('human')
        return await milk_bot.say('- Human -\n'
                                  'Attack Modifier: {}%\n'
                                  'Defense Modifier: {}%\n'
                                  'Recruitment Modifier: {}%\n'
                                  'Spy Modifier: {}%\n'
                                  'Sentry Modifier: {}%'.format(r.attack_mod*100,
                                                                r.defense_mod*100,
                                                                r.recruitment_mod*100,
                                                                r.spy_mod*100,
                                                                r.sentry_mod*100))
    elif 'orc' in msg.split(' ')[-1]:
        r = player.Race('orc')
        return await milk_bot.say('- Orc -\n'
                                  'Attack Modifier: {}%\n'
                                  'Defense Modifier: {}%\n'
                                  'Recruitment Modifier: {}%\n'
                                  'Spy Modifier: {}%\n'
                                  'Sentry Modifier: {}%'.format(r.attack_mod * 100,
                                                                r.defense_mod * 100,
                                                                r.recruitment_mod * 100,
                                                                r.spy_mod * 100,
                                                                r.sentry_mod * 100))
    elif 'dwarf' in msg.split(' ')[-1]:
        r = player.Race('dwarf')
        return await milk_bot.say('- Dwarf -\n'
                                  'Attack Modifier: {}%\n'
                                  'Defense Modifier: {}%\n'
                                  'Recruitment Modifier: {}%\n'
                                  'Spy Modifier: {}%\n'
                                  'Sentry Modifier: {}%'.format(r.attack_mod * 100,
                                                                r.defense_mod * 100,
                                                                r.recruitment_mod * 100,
                                                                r.spy_mod * 100,
                                                                r.sentry_mod * 100))
    elif 'nightelf' in msg.split(' ')[-1]:
        r = player.Race('nightelf')
        return await milk_bot.say('- Nightelf -\n'
                                  'Attack Modifier: {}%\n'
                                  'Defense Modifier: {}%\n'
                                  'Recruitment Modifier: {}%\n'
                                  'Spy Modifier: {}%\n'
                                  'Sentry Modifier: {}%'.format(r.attack_mod * 100,
                                                                r.defense_mod * 100,
                                                                r.recruitment_mod * 100,
                                                                r.spy_mod * 100,
                                                                r.sentry_mod * 100))
    else:
        return await milk_bot.send_message(ctx.message.author, 'Try !raceinfo [race] to show their stats.')


@milk_bot.command(pass_context=True)
async def castle(ctx, *args):
    msg = ctx.message.content
    user = str(ctx.message.author)
    if db.players.find({'name': user}).count() is 0:
        return await milk_bot.say('Your profile does not exist. Type !chaos newgame to create one.')
    elif 'upgrade' in msg.split(' ')[-1]:
        p = player.Player(user)
        c = player.Castle(user)
        if c.up_cost <= p.gold:
            c.upgrade_castle()
            return await milk_bot.say('Castle has been successfully upgraded to tier {}'.format(c.upgrade_tier))
        else:
            return await milk_bot.say('You do not have enough gold to upgrade your castle. You have {} gold but the '
                                      'upgrade costs {}.'.format(p.gold, c.up_cost))
    else:
        c = player.Castle(user)
        return await milk_bot.say('Your next castle upgrade costs: {} gold.'.format(c.up_cost))

@milk_bot.command(pass_context=True)
async def spy(ctx, *args):
    msg = ctx.message.content
    user = str(ctx.message.author)
    defender = str(msg.split(' ')[-1]).lower()
    attacker = user
    if attacker.split('#')[0].lower().split(' ')[0] in defender:
        return await milk_bot.say('Stop hitting yourself')
    elif defender in CHAOS_PLAYER_NAMES:
        intel = coc.spy_on_player(attacker, defender)
        return await milk_bot.say(intel)
    else:
        return await milk_bot.say('That player does not exist, please try again with a valid player.')

# Start the bot
milk_bot.run(secrets.token_id)
