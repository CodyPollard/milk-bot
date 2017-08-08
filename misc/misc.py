# misc.py handles all misc commands


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


if __name__ == "__main__":
    pass
