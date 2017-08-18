from pymongo import MongoClient
from CoC import equipment_info

# DB info
client = MongoClient()
db = client.coc


# Player #
class Player(object):

    def __init__(self, user, race=None):
        if db.players.find({'name': user}).count() is 0:
            # Initialize the player
            self.name = user
            self.race = race
            # Stats
            self.recruit_rate = 10
            self.attack_power, self.defense_power = 0, 0
            self.spy_power, self.sentry_power = 0, 0
            self.gold = 1000
            # Create user's castle and Army
            Castle(self.name)
            Army(self.name)
            self.update_stats()
            db.players.insert(self.__dict__)
        else:
            p = db.players.find_one({'name': user})
            self.name = user
            self.race = p['race']
            self.gold = p['gold']
            self.recruit_rate = p['recruit_rate']
            self.update_stats()

    def update_stats(self):
        r = Race(self.race)
        a = Army(self.name)
        c = Castle(self.name)
        self.attack_power = a.get_offensive_power()*r.attack_mod
        self.defense_power = (a.get_defensive_power()*r.defense_mod)+(c.defense*(a.get_defensive_power()*r.defense_mod))
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
        db.players.update_one({'name': self.name}, {'$inc': {'gold': self.recruit_rate}}, upsert=False)


class Castle(object):

    def __init__(self, user):
        if db.castles.find({'owner': user}).count() is 0:
            self.owner = user
            self.upgrade_tier = 1
            self.defense = self.upgrade_tier/10
            self.capacity = 1000
            self.up_cost = 750
            db.castles.insert_one(self.__dict__)
        else:
            self.c = db.castles.find_one({'owner': user})
            self.owner = self.c['owner']
            self.upgrade_tier = self.c['upgrade_tier']
            self.defense = self.c['defense']
            self.capacity = self.c['capacity']
            self.up_cost = self.c['up_cost']

    def update_castle(self):
        self.c = db.castles.find_one({'owner': self.c['owner']})

    def upgrade_castle(self):
        self.upgrade_tier += 1
        self.defense = self.upgrade_tier/10
        self.capacity = 1000+(1000*self.defense)
        db.castles.update({'owner': self.owner}, {'owner': self.owner, 'upgrade_tier': self.upgrade_tier,
                                                  'defense': self.defense, 'capacity': self.capacity,
                                                  'up_cost': self.up_cost}, upsert=False)
        db.players.update_one({'name': self.owner}, {'$inc': {'gold': -self.up_cost}}, upsert=False)
        self.up_cost = 750 + (750 * self.defense)
        self.update_castle()


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
            self.ow_short_sword = 2
            self.ow_flail = 0
            self.ow_halberd = 0
            self.ow_cavalry = 0
            # Defensive Weapons
            self.dw_kite_shield = 5
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
            self.a = db.armies.find_one({'owner': user})
            # Soldiers
            self.s_footman = self.a['s_footman']
            # Covert Units
            self.c_spy = self.a['c_spy']
            self.c_sentry = self.a['c_sentry']
            # Offensive Weapons
            self.ow_short_sword = self.a['ow_short_sword']
            self.ow_flail = self.a['ow_flail']
            self.ow_halberd = self.a['ow_halberd']
            self.ow_cavalry = self.a['ow_cavalry']
            # Defensive Weapons
            self.dw_kite_shield = self.a['dw_kite_shield']
            self.dw_spear = self.a['dw_spear']
            self.dw_tower_shield = self.a['dw_tower_shield']
            self.dw_full_armor = self.a['dw_full_armor']
            # Spy Tools
            self.st_rope = self.a['st_rope']
            self.st_grapple_hook = self.a['st_grapple_hook']
            self.st_short_bow = self.a['st_short_bow']
            # Sentry Tools
            self.sen_torch = self.a['sen_torch']
            self.sen_guard_dog = self.a['sen_guard_dog']
            self.sen_alarm = self.a['sen_alarm']

    def update_army(self):
        self.a = db.armies.find_one({'owner': self.a['owner']})

    def get_defensive_power(self):
        weapon_strength = self.get_defensive_weapons()[0]
        total_power = weapon_strength + int(self.__dict__['s_footman'])
        return total_power

    def get_defensive_weapons(self):
        weapon_strength = 0
        weapon_durability = 0
        ks = equipment_info.KiteShield()
        spear = equipment_info.Spear()
        ts = equipment_info.TowerShield()
        fa = equipment_info.FullArmor()
        weapon_strength += int(self.__dict__['dw_kite_shield']) * ks.strength
        weapon_strength += int(self.__dict__['dw_spear']) * spear.strength
        weapon_strength += int(self.__dict__['dw_tower_shield']) * ts.strength
        weapon_strength += int(self.__dict__['dw_full_armor']) * fa.strength
        weapon_durability += int(self.__dict__['dw_kite_shield']) * ks.durability
        weapon_durability += int(self.__dict__['dw_spear']) * spear.durability
        weapon_durability += int(self.__dict__['dw_tower_shield']) * ts.durability
        weapon_durability += int(self.__dict__['dw_full_armor']) * fa.durability
        return weapon_strength, weapon_durability

    def get_offensive_power(self):
        weapon_strength = self.get_offensive_weapons()[0]
        total_power = weapon_strength+int(self.__dict__['s_footman'])
        return total_power

    def get_offensive_weapons(self):
        weapon_strength = 0
        weapon_durability = 0
        ss = equipment_info.ShortSword()
        flail = equipment_info.Flail()
        hal = equipment_info.Halberd()
        cav = equipment_info.Cavalry()
        weapon_strength += int(self.__dict__['ow_short_sword'])*ss.strength
        weapon_strength += int(self.__dict__['ow_flail']) * flail.strength
        weapon_strength += int(self.__dict__['ow_halberd']) * hal.strength
        weapon_strength += int(self.__dict__['ow_cavalry']) * cav.strength
        weapon_durability += int(self.__dict__['ow_short_sword']) * ss.durability
        weapon_durability += int(self.__dict__['ow_flail']) * flail.durability
        weapon_durability += int(self.__dict__['ow_halberd']) * hal.durability
        weapon_durability += int(self.__dict__['ow_cavalry']) * cav.durability
        return weapon_strength, weapon_durability

    def get_spy_power(self):
        tool_strength = self.get_offensive_weapons()[0]
        total_power = tool_strength+int(self.__dict__['c_spy'])
        return total_power

    def get_spy_tools(self):
        tool_strength = 0
        tool_durability = 0
        rope = equipment_info.Rope()
        grap = equipment_info.GrappleHook()
        sb = equipment_info.ShortBow()
        tool_strength += int(self.__dict__['st_rope'])*rope.strength
        tool_strength += int(self.__dict__['st_grapple_hook']) * grap.strength
        tool_strength += int(self.__dict__['st_short_bow']) * sb.strength
        tool_durability += int(self.__dict__['st_rope']) * rope.durability
        tool_durability += int(self.__dict__['st_grapple_hook']) * grap.durability
        tool_durability += int(self.__dict__['st_short_bow']) * sb.durability
        return tool_strength, tool_durability

    def get_sentry_power(self):
        tool_strength = self.get_offensive_weapons()[0]
        total_power = tool_strength+int(self.__dict__['c_sentry'])
        return total_power

    def get_sentry_tools(self):
        tool_strength = 0
        tool_durability = 0
        torch = equipment_info.Torch()
        gd = equipment_info.GuardDog()
        alarm = equipment_info.Alarm()
        tool_strength += int(self.__dict__['sen_torch'])*torch.strength
        tool_strength += int(self.__dict__['sen_guard_dog']) * gd.strength
        tool_strength += int(self.__dict__['sen_alarm']) * alarm.strength
        tool_durability += int(self.__dict__['sen_torch'])*torch.durability
        tool_durability += int(self.__dict__['sen_guard_dog']) * gd.durability
        tool_durability += int(self.__dict__['sen_alarm']) * alarm.durability
        return tool_strength, tool_durability

    # Increments the user's footman count based on their recruitment_rate in Player
    def recruit_footman(self, inc):
        db.armies.update_one({'owner': self.a['owner']}, {'$inc': {'s_footman': inc}}, upsert=False)
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
    p = Player('onemore', 'human')
    c = Castle(p.name)
    a = Army(p.name)
    print(c.__dict__)
    print(p.gold)
    print(a.s_footman)
    print('Upgrading')
    print('----------------')
    p.recruit_loop()
    print(c.__dict__)
    print(p.gold)
    print(a.s_footman)