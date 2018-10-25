import sqlite3,  datetime, os

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = dir_path + '../tests/quotes.db'


# AddQuote handles the user input for a quote before it is added to a database
class QuoteAdd(object):
    def __init__(self, ctx):
        temp = ctx.split('"')
        self.msg = temp[1]
        self.author = temp[-1]
        self.call_count = 0

    def to_db(self):
        # Add quote to DB here
        return


# # DBQuote handles the usage of a quote after it has been added to a database by AddQuote
# class QuoteDB(object):
#
#     def __init__(self, _id=None):
#         if _id is None:
#             self.quote = None
#             print('No ID passed')
#         else:
#             self.quote = db.milk_quotes.find_one({'_id': _id})
#             print('ID was passed')


class UserProfile(object):
    def __init__(self, usr):
        conn = sqlite3.connect('met_test.db')
        cur = conn.cursor()
        print(cur.execute('select 1 from test_user_metrics where t_user=?'), (usr, ))



def create_quote_db():
    try:
        os.remove(db_path)
        print('DB removed')
    except FileNotFoundError:
        print('DB did not exist')

    conn = sqlite3.connect('quotes.db')


def test_populate_db():
    d = datetime.datetime
    # Delete DB before test
    try:
        os.remove(db_path)
        print('DB removed')
    except FileNotFoundError:
        print('DB did not exist')
    # Test
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    # Make table
    cur.execute('''CREATE TABLE test_quotes
                 (t_id integer primary key, t_date text, author varchar(30), quote text NOT NULL)''')
    # Insert a row
    # cur.execute("INSERT INTO test_quotes VALUES (1,?,'Kraine','Canada is O K A Y')", (str(d.today()),))
    # Execute Many
    many_quotes = [(str(d.today()), 'Kraine', 'Canada is O K A Y'),
                   (str(d.today()), 'Vanek', 'Buffalo sucks'),
                   (str(d.today()), 'Kraine', 'Once upon a time there was a man named humpty dumpty.'),
                  ]
    cur.executemany('INSERT INTO test_quotes(t_date, author, quote) VALUES (?,?,?)', many_quotes)
    # Save and close
    conn.commit()
    conn.close()


def test_read_db():
    # Open
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    # Read
    for row in cur.execute('select * from test_quotes order by t_id desc'):
        print(row)
    # Save and close
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # Tests
    # test_create_quote_db()
    UserProfile('Kraine')
