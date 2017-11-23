# misc.py handles all misc commands
import sqlite3, re
from sqlite3 import Error

# 8 Ball #
eightball = ['It is certain','It is decidedly so','Without a doubt','Yes definitely','You may rely on it','As I see it, yes',
                  'Most likely','Outlook good','Yes','Signs point to yes','Reply hazy try again','Ask again later',
                  'Better not tell you now','Cannot predict now','Concentrate and ask again',"Don't count on it",
                  'My reply is no','My sources say no','Outlook not so good','Very doubtful']


# Shopping List #
def write_shopping_list(msg):
    with open('shoppinglist.txt', 'a') as f:
        f.write(msg + '\n')


def get_shopping_list():
    slist = []
    with open('shoppinglist.txt', 'r') as f:
        slist.append(f.readline())

    return slist


# Ducks Injuries
def get_latest_injury():
    # Choose DB
    db = 'ducks.sqlite3'
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select headline from milk_ducksinjury order by id desc limit 1")
    latest = cur.fetchall()
    latest_str = [tup[0] for tup in latest]
    return latest_str[0]


if __name__ == "__main__":
    print(get_latest_injury())


