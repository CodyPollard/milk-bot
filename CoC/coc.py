from threading import Thread, Timer
from pymongo import MongoClient
from CoC import player
from collections import OrderedDict
from itertools import islice
import random


# DB info
client = MongoClient()
db = client.coc


# Combat equation used for any offensive action. Accepts 2 arguments, attacker's power and defender's power. Returns
# the % chance on a scale of 0-100 that the attacker succeeds.
def COMBAT(attacker, defender):
    A, B, C = 1, 1, 1
    win_chance = (A * ((2 * attacker + defender) / (attacker + defender)) +
         B * ((attacker + defender) / (2 * (attacker + defender))) -
         C * ((attacker + 2 * defender) / (attacker + defender))) * 100
    return win_chance


# Timer that updates a player's soldier count based on their recruitment_rate
def recruitment_cycle():
    for document in db.players.find():
        print(document)
        p = player.Player(document['name'])
        p.recruit_loop()
        print(p.attack_power)
    Timer(300, recruitment_cycle).start()


# Spying #
def spy_on_player(p1_att, p2_def):
    attacker = player.Player(p1_att)
    print(p2_def)
    temp_defender = db.players.find_one({'name': {'$regex': '^{}'.format(p2_def), '$options': 'im'}})
    print(temp_defender)
    defender = player.Player(temp_defender['name'])
    success_rate = 0
    # Check for outright success or failure
    if attacker.spy_power < defender.sentry_power*.5:
        print('Lost on first roll')
        return 'You Lost!'
    else:
        if attacker.spy_power < defender.sentry_power*1.5:
            success_rate = COMBAT(attacker.spy_power, defender.sentry_power)
            print('Won first roll.')
            if random.randint(0, 100) < success_rate:
                # Attacker wins
                print('Won second roll.')
                return spy_success(success_rate, defender)
            else:
                # Defender Wins
                print('Lost on second roll')
                return 'You Lost!'
        else:
            # 0% chance of failure when spy power is 50%+ over defenders sentry power
            # Return with info for the attacker
            print('Won outright.')
            return spy_success(random.randint(70, 100), defender)


def spy_failure(seed):
    # Do stuff to the attacker when they fail
    pass


def spy_success(seed, defender):
    # Gather intel based on seed given
    intel = []
    # Attack Power
    if random.randint(0, 100) <= seed:
        intel.append('Attack Power: {}'.format(defender.attack_power))
    # Defense Power
    if random.randint(0, 100) <= seed:
        intel.append('Defender Power: {}'.format(defender.defense_power))
    # Spy Power
    if random.randint(0, 100) <= seed:
        intel.append('Spy Power: {}'.format(defender.spy_power))
    # Sentry Power
    if random.randint(0, 100) <= seed:
        intel.append('Sentry Power: {}'.format(defender.sentry_power))
    # Units
    if random.randint(0, 100) <= seed:
        intel.append('Footmen: {}'.format(player.Army(defender.name).s_footman))
    # Gold
    if random.randint(0, 100) <= seed:
        intel.append('Gold: {}'.format(defender.gold))
    print('End of spy_success')
    print(intel)
    return intel


# Leaderboards #

def get_ranks():
    leaderboard = {}
    for document in db.players.find():
        p = player.Player(document['name'])
        leaderboard[p.name] = p.get_total_score()
    return OrderedDict(sorted(leaderboard.items(), key=lambda v: v[1], reverse=True))


def get_top_three():
    leaderboard = {}
    for document in db.players.find():
        p = player.Player(document['name'])
        leaderboard[p.name] = p.get_total_score()
    temp = OrderedDict(sorted(leaderboard.items(), key=lambda v: v[1], reverse=True))
    try:
        sliced = islice(temp.items(), 3)
        sliced_o = OrderedDict(sliced)
        return sliced_o
    except IndexError:
        return 'IE'

# Runs when the bot starts
if __name__ == '__main__':
    print('Started coc.py')
    print(spy_on_player('Riokishen#2325', 'Riokishen#2325'))