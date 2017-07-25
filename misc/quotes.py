import re
from pymongo import MongoClient
import random

client = MongoClient()
db = client.quotes
collection = db.milk_quotes


# AddQuotes #
class ValidationError(Exception):
    pass


# AddQuote handles the user input for a quote before it is added to a database
class AddQuote(object):
    def __init__(self, ctx):
        temp = ctx.split('"')
        self.msg = temp[1]
        self.author = temp[-1]
        self.call_count = 0

    def to_dict(self):
        return self.__dict__

    def to_mongo(self):
        collection.insert(self.to_dict())


# DBQuote handles the usage of a quote after it has been added to a database by AddQuote
class DBQuote(object):

    def __init__(self, _id=None):
        if _id is None:
            self.quote = None
            print('No ID passed')
        else:
            self.quote = db.milk_quotes.find_one({'_id': _id})
            print('ID was passed')

    # Returns a random quote from the collection milk_quotes. author is an optional argument and if given
    # will return a random quote from the given author
    def get_quote(self, author=None):
        if author is None:
            # Find random quote from entire collection
            collection_max = int(db.milk_quotes.find().count()) - 1
            rand_index = random.randint(0, collection_max)
            self.quote = db.milk_quotes.find()[rand_index]
            self.update_call_count()
            return self.quote
        else:
            # Find random quote by a given author
            sub_string = author[:4]
            regx = '.*' + sub_string + '.*'
            all_quotes = db.milk_quotes.find({'author': {'$regex': regx, '$options': 'i'}})
            quote_list = []
            for i in all_quotes:
                quote_list.append(i)

            # Check if there are any quotes found for the author and return a random one
            if not quote_list:
                raise ValidationError("Invalid Author")
            else:
                self.quote = random.choice(quote_list)
                self.update_call_count()
                return self.quote

    def update_call_count(self):
        db.milk_quotes.update_one({'_id': self.quote['_id']}, {'$inc': {'call_count': 1}}, upsert=False)
        self.quote = db.milk_quotes.find_one({'_id': self.quote['_id']})


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
    AddQuote(msg).to_mongo()


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
    d = DBQuote()
    d.get_quote('cody')
    print(d.quote['msg'])
    print(d.quote['call_count'])
