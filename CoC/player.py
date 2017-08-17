from pymongo import MongoClient

# DB info
client = MongoClient()
db = client.coc


# Player #
class Player(object):

    def __init__(self, user, race=None):
        if db.players.find({'name': user}).count() is 0:
            print('This user doesnt exist')
            # Initialize the player
            self.name = user
            self.race = race
            # Stats
            self.recruit_rate = 10
            self.attack_power, self.defense_power = 0, 0
            self.spy_power, self.sentry_power = 0, 0
            # Create user's castle and Army
            Castle(self.name)
            Army(self.name)
            self.update_stats()
            db.players.insert(self.__dict__)
        else:
            p = db.players.find_one({'name': user})
            self.name = user
            self.race = p['race']
            self.recruit_rate = p['recruit_rate']
            self.update_stats()

    def update_stats(self):
        r = Race(self.race)
        a = Army(self.name)
        self.attack_power = a.get_soldier_power()*r.attack_mod
        self.defense_power = a.get_soldier_power()*r.defense_mod
        self.spy_power = a.get_spy_power()*r.spy_mod
        self.sentry_power = a.get_sentry_power()*r.sentry_mod
        self.recruit_rate *= r.recruitment_mod

    def get_stats(self):
        return self.__dict__

    def get_total_score(self):
        c = Castle(self.name)
        return (self.attack_power+self.defense_power+self.spy_power+self.sentry_power)*(float(c.upgrade_tier)*.25)*10


    def recruit_loop(self):
        Army(self.name).recruit_footman(self.recruit_rate)


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
            c = db.castles.find_one({'owner': user})
            self.upgrade_tier = c['upgrade_tier']
            self.defense = c['defense']
            self.capacity = c['capacity']


class Army(object):

    def __init__(self, user):
        if db.armies.find({'owner': user}).count() is 0:
            self.owner = user
            # Soldiers
            self.s_footman = 100
            # Covert Units
            self.c_spy = 25
            self.c_sentry = 25
            # Offensive Weapons
            self.ow_short_sword = 0
            self.ow_flail = 0
            self.ow_halberd = 0
            self.ow_cavalry = 0
            # Defensive Weapons
            self.dw_kite_shield = 0
            self.dw_spear = 0
            self.dw_tower_shield = 0
            self.dw_full_armor = 0
            # Spy Tools
            self.st_rope = 0
            self.st_grapple_hook = 0
            self.st_short_bow = 0
            # Sentry Tools
            self.sen_torch = 0
            self.sen_guard_dog = 0
            self.sen_alarm = 0
            db.armies.insert_one(self.__dict__)
        else:
            a = db.armies.find_one({'owner': user})
            self.a_object = a
            # Soldiers
            self.s_footman = a['s_footman']
            # Covert Units
            self.c_spy = a['c_spy']
            self.c_sentry = a['c_sentry']
            # Offensive Weapons
            self.ow_short_sword = a['ow_short_sword']
            self.ow_flail = a['ow_flail']
            self.ow_halberd = a['ow_halberd']
            self.ow_cavalry = a['ow_cavalry']
            # Defensive Weapons
            self.dw_kite_shield = a['dw_kite_shield']
            self.dw_spear = a['dw_spear']
            self.dw_tower_shield = a['dw_tower_shield']
            self.dw_full_armor = a['dw_full_armor']
            # Spy Tools
            self.st_rope = a['st_rope']
            self.st_grapple_hook = a['st_grapple_hook']
            self.st_short_bow = a['st_short_bow']
            # Sentry Tools
            self.sen_torch = a['sen_torch']
            self.sen_guard_dog = a['sen_guard_dog']
            self.sen_alarm = a['sen_alarm']

    def update_army(self):
        self.a_object = db.armies.find_one({'owner': self.a_object['owner']})

    def get_soldier_power(self):
        # Get each unit count and multiply by unit strength from unitinfo
        total_power = self.__dict__['s_footman']
        print(total_power)
        # for i in self.__dict__:
        #     if str(i).startswith('s_'):
        #         total_power += self.__dict__[i]
        return total_power

    def get_spy_power(self):
        total_power = 0
        for i in self.__dict__:
            if str(i) == 'c_spy':
                total_power += self.__dict__[i]
        return total_power

    def get_sentry_power(self):
        total_power = 0
        for i in self.__dict__:
            if str(i) == 'c_sentry':
                total_power += self.__dict__[i]
        return total_power

    def recruit_footman(self, inc):
        # Increments the user's footman count based on their recruitment_rate in Player
        db.armies.update_one({'owner': self.a_object['owner']}, {'$inc': {'s_footman': inc}}, upsert=False)
        self.update_army()


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


def set_race(r):
    if r == 'human':
        return [1.0, 1.0, 1.5, 1.25, 1.25]
    elif r == 'dwarf':
        return [1.0, 1.75, 1.0, 1.0, 1.25]
    elif r == 'orc':
        return [1.5, 1.25, 1.0, 1.0, 1.0]
    elif r == 'nightelf':
        return [1.0, 1.0, 1.25, 1.75, 1.0]


if __name__ == '__main__':
    # DO THREADING SHIT HERE? #
    p = Player('onemore', 'human')
    Army(p.name).get_soldier_power()
