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
                 (p_id integer primary key, username text, cmd_quote int, cmd_eightball int, cmd_add int, alias text)''')
    # Insert a row
    cur.execute('INSERT INTO profiles(username, cmd_quote, cmd_eightball, cmd_add, alias) VALUES (?,?,?,?,?)',
                ('admin', 7, 7, 7, 'admin_alias'))
    # Save and close
    conn.commit()
    conn.close()


def read_db():
    conn = sqlite3.connect('user_metrics.db')
    cur = conn.cursor()
    db_list = []
    for row in cur.execute('select * from profiles order by p_id desc'):
        db_list.append(row)
        print(row)
    conn.commit()
    conn.close()
    return db_list


def update_tables():
    conn = sqlite3.connect('user_metrics.db')
    cur = conn.cursor()
    cur.execute('alter table profiles add column "alias" "text"')


# Returns a list of alias for a given profile or matching alias
def get_alias(name):
    # Open
    conn = sqlite3.connect('user_metrics.db')
    cur = conn.cursor()
    if UserProfile(name).user_exists():
        # Get listed alias for this user
        print('This is a profile name')
        alias = ''
        for row in cur.execute('select alias from profiles where username=?', (name,)):
            alias = list(row[0].split(','))
        return alias
    else:
        # Try to match given alias to existing profile
        print('Checking alias of existing profiles for match.')
        for row in cur.execute('select alias, username from profiles'):
            if name in row[0]:
                print('Found match with profile {}'.format(row[1]))
                return list(row[0].split(','))
        return 'No matches found for given name'


class UserProfile(object):
    def __init__(self, usr):
        self.usr = str(usr).lower()

    def user_exists(self, alt_user=None):
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        if alt_user is None:
            print('Alt User is None')
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
        else:
            print('Alt user is {}'.format(alt_user))
            cur.execute('select count(*) from profiles where username=?', (alt_user,))
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

    def alias_exists(self, name):
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        # Try to match given alias to existing profile
        print('Checking alias of existing profiles for match.')
        for row in cur.execute('select alias from profiles'):
            print('ALIAS EXISTS ROW ZERO: {} NAME: {}'.format(row[0], name))
            for i in row:
                for j in i.split(','):
                    if j == name:
                        return True
        # No match found
        return False

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
            cur.execute('INSERT INTO profiles(username, cmd_quote, cmd_eightball, cmd_add, alias) VALUES (?,?,?,?,?)',
                        (self.usr, 0, 0, 0, self.usr, ))
            # Save and close
            conn.commit()
            conn.close()
            return 'Profile created.'

    def inject_profile(self, alt_user):
        read_db()
        print('Injecting alt_user: {}'.format(alt_user))
        # Check if user exists and create new profile if they don't
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        if self.user_exists(alt_user):
            # Save and close
            conn.commit()
            conn.close()
            return 'Your profile already exists.'
        else:
            cur.execute('INSERT INTO profiles(username, cmd_quote, cmd_eightball, cmd_add, alias) VALUES (?,?,?,?,?)',
                        (alt_user, 0, 0, 0, alt_user, ))
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
        for row in cur.execute('select cmd_quote, cmd_eightball, cmd_add, alias from profiles where username=?', (self.usr,)):
            stat_list = row
        # Save and close
        conn.commit()
        conn.close()
        return stat_list

    def add_alias(self, alias):
        conn = sqlite3.connect('user_metrics.db')
        cur = conn.cursor()
        alias = alias.strip().lower()
        a = cur.execute('select alias from profiles where username=?', (self.usr,))
        old_alias = a.fetchone()
        print('OLD ALIAS: {}'.format(old_alias))
        # Initialize Alias if it's empty
        if old_alias is None:
            print('Empty Alias Column')
            cur.execute('update profiles set alias=? where username=?', (self.usr, self.usr,))
        print(cur.execute('select alias from profiles where username=?', (self.usr,)).fetchall())
        # Check if alias already exists
        if self.alias_exists(alias):
            return 'Alias already exists.'
        # Add new alias
        a = cur.execute('select alias from profiles where username=?', (self.usr,))
        old_alias = a.fetchone()
        new_alias = ''
        for i in old_alias:
            new_alias = new_alias + str(i) + ','
        new_alias = new_alias + alias
        cur.execute('update profiles set alias=? where username=?', (new_alias, self.usr,))
        # Save and close
        conn.commit()
        conn.close()
        # print('Alias:{}\nAlias_List:{}'.format(alias, new_alias))
        return '{} is now an alias of {}'.format(alias, self.usr)


if __name__ == '__main__':
    initialize_user_metrics_db()
    read_db()
    # Test get_profile
    p = UserProfile('cody pollard')
    p.create_profile()
    print(p.add_alias('cody'))
    print('----------ADDING EXISTING ALIAS-----------')
    print(p.add_alias('cody'))
    read_db()
    # print(get_alias('abc123'))

