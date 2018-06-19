import os
import json, logging
# misc Settings
PROGRAM_PATH = os.path.dirname(os.path.realpath(__file__))
MISC_PATH = PROGRAM_PATH+'/misc/'

# Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# Create a file handler
handler = logging.FileHandler(PROGRAM_PATH + '/settings.log')
handler.setLevel(logging.DEBUG)
# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Add the handlers to the logger
logger.addHandler(handler)


class Settings(object):

    def __init__(self):
        # Read settings from settings.json
        logger.info('Initializing Settings')
        try:
            with open(PROGRAM_PATH + '/settings.json') as f:
                data = json.load(f)
        except OSError as e:
            logger.error(e)
        # Set values
        logger.debug('Assinging settings')
        self.admins = data['admins']
        self.quote_interval = data['quote_interval']

    def is_admin(self, author):
        # Check if user issuing command is an admin
        if author in self.admins:
            return True
        else:
            return False

    def get_quote_interval(self):
        return self.quote_interval

    def validate_quote_interval(self, x):
        # Check if interval given is an int in the valid range
        if isinstance(x, int) and 1 <= x <= 12:
            return True
        else:
            return False

    def set_quote_interval(self, x):
        # Write new interval into settings.json after validation
        with open(PROGRAM_PATH + '/settings.json', 'r+') as f:
            data = json.load(f)
            data['quote_interval'] = x
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def set_admin(x):
        # Add admin to list of existing admins
        with open(PROGRAM_PATH + '/settings.json', 'r+') as f:
            data = json.load(f)
            data['admins'].append(x)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

# if __name__ == '__main__':
