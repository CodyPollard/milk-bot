from settings import MISC_PATH
quote_list = []


# Quotes #
class ValidationError(Exception):
    pass


class Quote(object):
    def __init__(self, ctx):
        self.id = 0
        temp = ctx.split('"')
        self.msg = temp[1]
        self.author = temp[-1]


def update_quotes():
    with open(MISC_PATH+'quotes.txt', 'r') as f:
        for line in f:
            line.rstrip('\n')
            quote_list.append(line)

def add_quote(msg):
    # Validate that the given quote has quotation marks and an author
    if '"' in msg:
        q = Quote(msg)
        if '-' in q.author:
            # Write the quote to quotes.txt and strip the !add prefix
            with open(MISC_PATH+'quotes.txt', 'a') as f:
                f.write('\n')
                f.write(q.msg + ' ' + q.author)
            update_quotes()
            return True
        else:
            raise ValidationError('Please add an author at the end of your quote.')
    else:
        raise ValidationError('Please use quotation marks when adding a quote.')


if __name__ == "__main__":
    q = Quote('!add "This is a quote" -Bot')
    print(q.author)
    print(q.msg)