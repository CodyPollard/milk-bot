# Unit info file to hold various stats about unit types in CoC


# Soldiers #

class Footman:
    description = "Basic soldier with limited offensive and defensive capabilities. The default unit that can be" \
                  "given weapons to increase either your defensive or offensive power but not both."
    strength = 1
    hp = 5


# Spy
class Spy:
    description = "Standard offensive covert unit available to all players from the start. Spies are used" \
                  "to gain intelligence on an enemy and in some cases can sabotage enemy Soldier's weapons. A " \
                  "sabotaged weapon will break when used giving the soldier no bonus damage. It will not show " \
                  "up as broken until the unit uses it in battle giving you an offensive edge."
    strength = 5
    hp = 20


# Sentry
class Sentry:
    description = "Standard defensive covert unit available to all players from the start. Sentries are used " \
                  "to defend against enemy spies and can sometimes capture multiple spies given a large enough " \
                  "strength advantage."
    strength = 5
    hp = 20

