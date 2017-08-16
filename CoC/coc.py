from threading import Thread, Timer
from pymongo import MongoClient
from CoC import player

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


# Runs when the bot starts
if __name__ == '__main__':
    print('Started coc.py')
    recruitment_cycle()