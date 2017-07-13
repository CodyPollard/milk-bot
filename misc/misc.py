# quotes.py handles the reading and writing of quotes.txt
# Used by the bot's !quote command
from settings import MISC_PATH
quote_list = []

class ValidationError(Exception):
    pass

# Open quotes.txt and read the contents into quote_list
def update_quotes():
    with open(MISC_PATH+'quotes.txt', 'r') as f:
        for line in f:
            line.rstrip('\n')
            quote_list.append(line)

def add_quote(msg):
    if '"' in msg:
        print('This contains quotes')
        new = msg.split(" ")
        if '-' in new[len(new)-1]:
            print("Thanks for adding an author")
            with open(MISC_PATH+'quotes.txt', 'r') as f:
                f.write('\n')
                for i in range(1, len(new)):
                    f.write(new[i] + " ")
            update_quotes()
            return True
        else:
            raise ValidationError('Please add an author at the end of your quote.')
    else:
        raise ValidationError('Please use quotation marks when adding a quote.')

if __name__ == "__main__":
    pass