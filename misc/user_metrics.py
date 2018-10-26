import sqlite3, os

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = dir_path + '/user_metrics.db'


def initialize_user_metrics_db():
    # Delete DB before initializing
    try:
        os.remove(db_path)
        print('DB removed')
    except FileNotFoundError:
        print('DB did not exist')
    # Test
    conn = sqlite3.connect('user_metrics.db')
    cur = conn.cursor()
    # Make table
    cur.execute('''CREATE TABLE profiles
                 (p_id integer primary key, username text, cmd_quote int, cmd_eightball int, cmd_add int)''')
    # Insert a row
    cur.execute('INSERT INTO profiles(username, cmd_quote, cmd_eightball, cmd_add) VALUES (?,?,?,?)',
                ('admin', 7, 7, 7,))
    # Save and close
    conn.commit()
    conn.close()


def read_db():
    conn = sqlite3.connect('user_metrics.db')
    cur = conn.cursor()
    db_list = []
    for row in cur.execute('select * from profiles order by p_id desc'):
        db_list.append(row)
    conn.commit()
    conn.close()
    return db_list


class UserProfile(object):
    def __init__(self, usr):
        self.usr = str(usr).lower()

    def user_exists(self):
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        cur.execute('select count(*) from profiles where username=?', (self.usr,))
        data = cur.fetchone()[0]
        if data == 0:
            # Save and close
            conn.commit()
            conn.close()
            return False
        else:
            # Save and close
            conn.commit()
            conn.close()
            return True

    def create_profile(self):
        read_db()
        # Check if user exists and create new profile if they don't
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        if self.user_exists():
            # Save and close
            conn.commit()
            conn.close()
            return 'Your profile already exists.'
        else:
            cur.execute('INSERT INTO profiles(username, cmd_quote, cmd_eightball, cmd_add) VALUES (?,?,?,?)',
                        (self.usr, 0, 0, 0, ))
            # Save and close
            conn.commit()
            conn.close()
            return 'Profile created.'

    def increment_quote(self):
        # Open
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        # Increment cmd_quote by 1
        cur.execute('UPDATE profiles SET cmd_quote=cmd_quote+1 WHERE username=?', (self.usr,))
        # Save and close
        conn.commit()
        conn.close()

    def increment_add(self):
        # Open
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        # Increment cmd_add by 1
        cur.execute('UPDATE profiles SET cmd_add=cmd_add+1 WHERE username=?', (self.usr,))
        # Save and close
        conn.commit()
        conn.close()

    def increment_eightball(self):
        # Open
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        # Increment cmd_eightball by 1
        cur.execute('UPDATE profiles SET cmd_eightball=cmd_eightball+1 WHERE username=?', (self.usr,))
        # Save and close
        conn.commit()
        conn.close()

    def get_profile(self):
        # Open
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        for row in cur.execute('select cmd_quote, cmd_eightball, cmd_add from profiles where username=?', (self.usr,)):
           stat_list = row
        # Save and close
        conn.commit()
        conn.close()
        return stat_list


if __name__ == '__main__':
    initialize_user_metrics_db()
    read_db()
    # Test get_profile
    p = UserProfile('Kraine')
    p.create_profile()
    print(p.get_profile())

