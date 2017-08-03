# Unit info file to hold various stats about unit types in CoC


# Soldiers #

class Footman:
    description = "First tier soldier with basic offensive and defensive capabilities. The cheapest to recruit with\n" \
                  " the lowest stats of all soldiers."
    strength = 5
    hp = 20


class Swordsman:
    description = "Second tier soldier with basic offensive and defensive capabilities."
    strength = 10
    hp = 40


class Lancer:
    description = "Third tier soldier with average offensive and defensive capabilities."
    strength = 25
    hp = 100


class Knight:
    description = "Fourth tier soldier with high offensive and defensive capabilities."
    strength = 50
    hp = 200


class RoyalGuard:
    description = "Fifth tier soldier with basic offensive and defensive capabilities. The most expensive to recruit\n" \
                  "with the highest stats of any soldier"
    strength = 100
    hp = 400


# Spy
class Spy:
    description = "Standard offensive covert unit available to all players from the start. Spies are used \n" \
                  "to gain intelligence on an enemy and in some cases can sabotage enemy Soldier's weapons. A \n" \
                  "sabotaged weapon will break when used giving the soldier no bonus damage. It will not show \n" \
                  "up as broken until the unit uses it in battle giving you an offensive edge."
    strength = 5
    hp = 20


# Sentry
class Sentry:
    description = "Standard defensive covert unit available to all players from the start. Sentries are used \n" \
                  "to defend against enemy spies and can sometimes capture multiple spies given a large enough \n" \
                  "strength advantage."
    strength = 5
    hp = 20

