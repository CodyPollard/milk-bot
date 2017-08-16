from discord.ext.commands import Bot
from misc import misc, quotes, crypto
from CoC import player, coc
import random, secrets, os
from pymongo import MongoClient

# DB info
client = MongoClient()
db = client.coc

milk_bot = Bot(command_prefix="!")
eight = misc.eightball

@milk_bot.event
async def on_ready():
    print("Client logged in")
    coc.recruitment_cycle()


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


@milk_bot.command(pass_context=True)
async def summary(ctx, *args):
    """Coming Soon"""
    market = ctx.message.content.split(' ')
    data = crypto.Market(market[1]).get_market_summary()
    return await milk_bot.say('USDT-BTC Summary\n'
                              'Last Sale: ${}\n'
                              'Daily Delta: {:+.2f}%'.format(data[0], data[1]))


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
            player.Player(user, str(race.content))
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
                                                               'Swordsmen: {}\n'
                                                               'Lancers: {}\n'
                                                               'Knights: {}\n'
                                                               'Royal Guard: {}\n'
                                                               '- Covert -\n'
                                                               'Spies: {}\n'
                                                               'Sentries: {}'.format(a.s_footman, a.s_swordsman,
                                                                                     a.s_lancer, a.s_knight,
                                                                                     a.s_royal_guard, a.c_spy,
                                                                                     a.c_sentry))
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
                                                               'Attack Power: {}\n'
                                                               'Defense Power: {}\n'
                                                               'Spy Power: {}\n'
                                                               'Sentry Power: {}'.format(p.race, p.recruit_rate,
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

# Start the bot
milk_bot.run(secrets.token_id)
