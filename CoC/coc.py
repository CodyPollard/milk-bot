from threading import Thread, Timer
from pymongo import MongoClient
from CoC import player
from collections import OrderedDict
from itertools import islice

# DB info
client = MongoClient()
db = client.coc


# Timer that updates a player's soldier count based on their recruitment_rate
def recruitment_cycle():
    for document in db.players.find():
        print(document)
        p = player.Player(document['name'])
        p.recruit_loop()
        print(p.attack_power)
    Timer(10, recruitment_cycle).start()

def get_ranks():
    leaderboard = {}
    for document in db.players.find():
        p = player.Player(document['name'])
        leaderboard[p.name] = p.get_total_score()
        #print(leaderboard[p.name])
    return OrderedDict(sorted(leaderboard.items(), key=lambda v: v[1], reverse=True))

def get_top_three():
    leaderboard = {}
    for document in db.players.find():
        p = player.Player(document['name'])
        leaderboard[p.name] = p.get_total_score()
    temp = OrderedDict(sorted(leaderboard.items(), key=lambda v: v[1], reverse=True))
    sliced = islice(temp.items(), 3)
    sliced_o = OrderedDict(sliced)
    return sliced_o

# Runs when the bot starts
if __name__ == '__main__':
    print('Started coc.py')
    lead_list = get_top_three()
    print(lead_list)
    # for i in lead_list:
    #     print(i, lead_list[i])

