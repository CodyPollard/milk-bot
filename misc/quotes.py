# Quotes #

class Quote(object):
    def __init__(self, ctx):
        self.id = 0
        temp = ctx.split('"')
        self.msg = temp[1]
        self.author = temp[-1]

if __name__ == "__main__":
    q = Quote('!add "This is a quote" -Bot')
    print(q.author)
    print(q.msg)