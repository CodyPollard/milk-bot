# quotes.py handles the reading and writing of quotes.txt
# Used by the bot's !quote command
from settings import MISC_PATH
from misc import quotes
quote_list = []

# Used for validating in add_quote
class ValidationError(Exception):
    pass

# Quotes #
# Open quotes.txt and read the contents into quote_list
def update_quotes():
    with open(MISC_PATH+'quotes.txt', 'r') as f:
        for line in f:
            line.rstrip('\n')
            quote_list.append(line)

def add_quote(msg):
    # Validate that the given quote has quotation marks and an author
    if '"' in msg:
        newMsg = msg.split('"')
        if '-' in newMsg[len(newMsg)-1]:
            # Write the quote to quotes.txt and strip the !add prefix
            with open(MISC_PATH+'quotes.txt', 'a') as f:
                f.write('\n')
                for i in range(1, len(newMsg)):
                    f.write(newMsg[i] + " ")
            update_quotes()
            return True
        else:
            raise ValidationError('Please add an author at the end of your quote.')
    else:
        raise ValidationError('Please use quotation marks when adding a quote.')

# 8 Ball #
eightball = ['It is certain','It is decidedly so','Without a doubt','Yes definitely','You may rely on it','As I see it, yes',
                  'Most likely','Outlook good','Yes','Signs point to yes','Reply hazy try again','Ask again later',
                  'Better not tell you now','Cannot predict now','Concentrate and ask again',"Don't count on it",
                  'My reply is no','My sources say no','Outlook not so good','Very doubtful']

if __name__ == "__main__":
    q = quotes.Quote('!add "Testing Quote" -Bot')
    pass
