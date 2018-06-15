import os
import json
# misc Settings
PROGRAM_PATH = os.path.dirname(os.path.realpath(__file__))
MISC_PATH = PROGRAM_PATH+'/misc/'


class Settings(object):

    def __init__(self):
        # Read settings from settings.json
        try:
            with open(PROGRAM_PATH + '/settings.json') as f:
                data = json.load(f)
        except OSError as e:
            print(e)
        # Set values
        print('Assigning settings')
        self.admins = data['admins']
        # print(self.admins[0])
        self.quote_interval = data['quote_interval']
        # print(self.quote_interval)

    # def is_admin(self):
    #     # Check if user issuing command is an admin
    #     return bool

    @staticmethod
    def validate_quote_interval(self, x):
        # Check if interval given is an int in the valid range
        if isinstance(x, int) and 1 <= x <= 12:
            return True
        else:
            return False

    @staticmethod
    def set_quote_interval(self, x):
        # Write new interval into settings.json after validation
        with open(PROGRAM_PATH + '/settings.json', 'r+') as f:
            data = json.load(f)
            data['quote_interval'] = x
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    @staticmethod
    def set_admin(x):
        # Add admin to list of existing admins
        with open(PROGRAM_PATH + '/settings.json', 'r+') as f:
            data = json.load(f)
            data['admins'].append(x)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

# if __name__ == '__main__':
