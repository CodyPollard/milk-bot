from pymongo import MongoClient

# DB info
client = MongoClient()
db = client.coc


def new_game(user, race):
    Player(user, race)


# Player #
class Player(object):

    def __init__(self, user, race=None):
        if db.players.find({'user': user}).count() is 0:
            print('This user doesnt exist')
            # Initialize the player
            self.name = user
            self.race = race
            # Units
            self.army = 100
            self.espionage = 25
            # Stats
            self.attack_power, self.defense_power = 100, 100
            self.spy_power, self.sentry_power = 25, 25
            # Create user's castle
            Castle(user)
            print(self.__dict__)
            db.players.insert(self.__dict__)

        else:
            print('This user exists')


    def update_stats(self):
        pass



class Castle(object):

    def __init__(self, user):
        if db.castles.find({'owner': user}).count() is 0:
            self.owner = user
            self.upgrade_tier = 1
            self.defense = 1000
            self.capacity = 1000
            db.castles.insert_one(self.__dict__)
            print('Castle did not exist but has been created')
        else:
            print(db.castles.find_one({'owner': user}))




# Used for initializing the race_col collection #
class Race(object):

    # Mods returned in order: attack, defense, recruitment, spy, sentry
    def __init__(self, r):
        stats = set_race(r)
        self.race = r
        self.attack_mod = stats[0]
        self.defense_mod = stats[1]
        self.recruitment_mod = stats[2]
        self.spy_mod = stats[3]
        self.sentry_mod = stats[4]
        print(self.__dict__)


def set_race(r):
    if r is 'human':
        return [1.0, 1.0, 1.5, 1.25, 1.25]
    elif r is 'dwarf':
        return [1.0, 1.75, 1.0, 1.0, 1.25]
    elif r is 'orc':
        return [1.5, 1.25, 1.0, 1.0, 1.0]
    elif r is 'nightelf':
        return [1.0, 1.0, 1.25, 1.75, 1.0]


if __name__ == '__main__':
    Player('test', 'orc')