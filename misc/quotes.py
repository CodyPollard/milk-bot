import re

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
def get_random_quote():
    collection_max = int(db.milk_quotes.find().count())-1
    rand_index = random.randint(0, collection_max)
    return db.milk_quotes.find()[rand_index]

def get_author_quote(a):
    sub_string = a[:4]
    regx = '.*'+sub_string+'.*'
    all = db.milk_quotes.find({'author': {'$regex': regx, '$options': 'i'}})
    quote_list = []
    for i in all:
        quote_list.append(i)

    if not quote_list:
        raise ValidationError("Invalid Author")
    else:
        rand_quote = random.choice(quote_list)
        update_call_count(rand_quote)
        return rand_quote


def print_quote():
    # Used by main.py to display a quote and increments call_count by 1
    rand_quote = get_random_quote()
    update_call_count(rand_quote)
    t = db.milk_quotes.find_one({'_id': rand_quote['_id']})
    print('End of print_quote')
    print(t['_id'])
    return t


def update_call_count(q):
    db.milk_quotes.update_one({'_id': q['_id']}, {'$inc': {'call_count': 1}}, upsert=False)


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


# Accepts message after validation to add to collection
def add_quote(msg):
    Quote(msg).to_mongo()


# Updates total count of quotes called
def get_call_count_total():
    call_total = 0
    for i in range(0,db.milk_quotes.find().count()):
        temp = db.milk_quotes.find()[i]
        call_total = call_total+int(temp['call_count'])
    return call_total


# Used to convert an old quotes.txt file to the new DB
def convert_txt():
    with open('quotes.txt', 'r+') as f:
        for line in f:
            n = line.rstrip()
            add_quote(n)


# Return a list of unique authors from all quotes in collection
def get_unique_authors():
    collection_max = int(db.milk_quotes.find().count()) - 1
    all_authors = []
    unique_authors = []
    for i in range(0, collection_max):
        # Get the author from each quote in the collection
        d = db.milk_quotes.find({}, {'author': 1, '_id': 0})[i]
        stripped = d['author'].split('-')[-1]
        # Trim the leading character if it is a space
        if re.match(r'[ \t]', stripped):
            all_authors.append(stripped.strip())
        else:
            all_authors.append(stripped)

    # Get list of unique authors by name
    for j in all_authors:
        print('Starting J loop')
        sub_string = j[:4]
        if any(sub_string in s for s in unique_authors):
            print("Author already added")
        else:
            unique_authors.append(j)

    return unique_authors

if __name__ == "__main__":
    print(get_author_quote('tolstoy'))
