import random, re
import sqlite3,  datetime, os
from . import user_metrics

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = dir_path + '/quotes.db'
regex = re.compile('[^a-zA-Z]')


class ValidationError(Exception):
    pass


# Validate that the given quote has quotation marks and an author
def validate_quote(msg, profile):
    # Get the first and last quote in a given message from the user
    start_index = msg.find('\"')
    end_index = 0
    for i, character in enumerate(msg):
        if character == '"':
            end_index = i
    # Check if the first and last quote found are not the same
    if start_index != -1 and end_index != start_index:
        full_quote = msg[start_index+1:end_index]
        new = msg.split('"')
        if '-' in new[-1]:
            if validate_author(new[-1]):
                # Adds the quote to collection after validation success
                q = Quote(datetime.datetime.now(), profile, full_quote, new[-1], 0)
                q.add_quote()
                return True
            else:
                raise ValidationError('Profile does not exist for the given author, please create a profile or add an '
                                      'alias for the author before submitting their quote.')
        else:
            raise ValidationError('Please add an author at the end of your quote.')
    else:
        raise ValidationError('Please use quotation marks around the entire quote.')


# Validate that the author of the quote exists in user_metrics.db. All quotes must be represented by a profile.
def validate_author(msg):
    author = regex.sub('', msg).lower()
    u = user_metrics.UserProfile(author)
    print(u.usr)
    if u.user_exists():
        return True
    elif author in user_metrics.get_alias(author):
        return True
    else:
        return False


# AddQuote handles the user input for a quote and adds it to a database
class Quote(object):
    def __init__(self, add_date, add_profile, quote, author, call_count):
        self.add_date = str(add_date)
        self.add_profile = str(add_profile)
        self.quote = quote
        self.author = regex.sub('', author).lower()
        self.call_count = call_count

    def add_quote(self):
        # Add validated quote to DB
        # Open
        conn = sqlite3.connect('quotes.db')
        cur = conn.cursor()
        # Insert a row
        cur.execute('INSERT INTO milk_quotes(add_date, add_profile, quote, author, call_count) VALUES (?,?,?,?,?)',
                    (self.add_date, self.add_profile, self.quote, self.author, 0,))
        # Save and close
        conn.commit()
        conn.close()


def get_random_quote():
    # Open
    conn = sqlite3.connect('quotes.db')
    cur = conn.cursor()
    # Get row count
    cur.execute('select count(*) from milk_quotes')
    max_id = cur.fetchone()[0]
    r_id = random.randint(2, max_id)
    print('Max: {}\nRID: {}'.format(max_id, r_id))
    q = cur.execute('select quote, author from milk_quotes where q_id=?', (r_id,))
    # Returns tuple of ('quote', 'author',)
    random_quote = q.fetchall()
    # Save and close
    conn.commit()
    conn.close()
    increment_call_count(r_id)
    return random_quote


def increment_call_count(q_id):
    conn = sqlite3.connect('quotes.db')
    cur = conn.cursor()
    cur.execute('UPDATE milk_quotes SET call_count=call_count+1 WHERE q_id=?', (q_id,))
    conn.commit()
    conn.close()


def initialize_quote_db():
    wipe_db()
    conn = sqlite3.connect('quotes.db')
    cur = conn.cursor()
    # Make table
    cur.execute('''CREATE TABLE milk_quotes
                     (q_id integer primary key, add_date text, add_profile text, quote text not null, author text, call_count int)''')
    # Insert a row
    cur.execute('INSERT INTO milk_quotes(add_date, add_profile, quote, author, call_count) VALUES (?,?,?,?,?)',
                ('1/1/2000', 'admin', 'quote', 'author', 0,))
    # Save and close
    conn.commit()
    conn.close()


def wipe_db():
    try:
        os.remove('quotes.db')
        print('DB removed')
    except FileNotFoundError:
        print('DB did not exist')


def read_db():
    # Open
    conn = sqlite3.connect('quotes.db')
    cur = conn.cursor()
    quote_list = []
    # Read
    for row in cur.execute('select * from milk_quotes order by q_id desc'):
        quote_list.append(row)
    # Save and close
    conn.commit()
    conn.close()
    return quote_list


if __name__ == '__main__':
    # Tests
    # Profile Creation

    user_metrics.initialize_user_metrics_db()
    u = user_metrics.UserProfile('Cody pollard')
    u.create_profile()
    u.add_alias('cody')
    user_metrics.read_db()
    # # Quote Creation
    wipe_db()
    initialize_quote_db()


















