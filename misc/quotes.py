from pymongo import MongoClient
import random

client = MongoClient()
db = client.quotes
collection = db.milk_quotes


# Quotes #
class ValidationError(Exception):
    pass


class Quote(object):

    def __init__(self, ctx):
        temp = ctx.split('"')
        self.msg = temp[1]
        self.author = temp[-1]
        self.call_count = 0

    def to_dict(self):
        return self.__dict__

    def to_mongo(self):
        collection.insert(self.to_dict())


# Used by main.py to get a random quote for the !quote command #
# Gets the max size of the collection -1 and picks a quote
# at that index for use
def get_random():
    collection_max = int(db.milk_quotes.find().count())-1
    rand_index = random.randint(0, collection_max)
    return db.milk_quotes.find()[rand_index]


def print_quote():
    # Used by main.py to display a quote and increments call_count by 1
    rand_quote = get_random()
    db.milk_quotes.update_one({'_id': rand_quote['_id']}, {'$inc': {'call_count': 1}}, upsert=False)
    t = db.milk_quotes.find({'_id': rand_quote['_id']})
    return t


# Validate that the given quote has quotation marks and an author
def validate_quote(msg):
    if '"' in msg:
        new = msg.split('"')
        if '-' in new[-1]:
            print('Successful Validation!')
            # Adds the quote to collection after validation success
            add_quote(msg)
            return True
        else:
            raise ValidationError('Please add an author at the end of your quote.')
    else:
        raise ValidationError('Please use quotation marks when adding a quote.')


def add_quote(msg):
    # Accepts message after validation to add to collection
    Quote(msg).to_mongo()


def get_call_count_total():
    call_total = 0
    for i in range(0,db.milk_quotes.find().count()-1):
        temp = db.milk_quotes.find()[i]
        call_total = call_total+int(temp['call_count'])
    return call_total

def convert_txt():
    with open('quotes.txt', 'r+') as f:
        for line in f:
            n = line.rstrip()
            add_quote(n)

if __name__ == "__main__":
    convert_txt()
