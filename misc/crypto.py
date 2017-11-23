import json, datetime
from urllib.request import urlopen


# def get_markets():
#     p = urlopen("https://bittrex.com/api/v1.1/public/getmarkets").read().decode('utf-8')
#     j = json.loads(p)
#     with open('all_markets.txt', 'w') as f:
#         json.dump(j, f, indent=4)
#
#
# def get_btc_orderbook():
#     p = urlopen('https://bittrex.com/api/v1.1/public/getorderbook?market=BTC-LTC&type=both').read().decode('utf-8')
#     j = json.loads(p)
#     with open('btc_orderbook.txt', 'w') as f:
#         json.dump(j, f, indent=4)
#
#
def get_NEO_history():
    p = urlopen('https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=usdt-btc&tickInterval=day').read().decode('utf-8')
    j = json.loads(p)
    with open('doge_history.txt', 'w') as f:
        json.dump(j, f, indent=4)


def get_btc_summary():
    p = urlopen('https://bittrex.com/api/v1.1/public/getmarketsummary?market=usdt-btc').read()
    j = json.loads(p)
    data = j['result'][0]
    last_sale = int(data['Last'])
    day_high = data['High']
    day_low = data['Low']
    prev_day = int(data['PrevDay'])
    perror = (last_sale-prev_day)/prev_day*100
    results = [last_sale, perror]
    return results


def btc_conversion(x):
    p = urlopen('https://bittrex.com/api/v1.1/public/getmarketsummary?market=usdt-btc').read()
    j = json.loads(p)
    data = j['result'][0]
    last_sale = int(data['Last'])
    return x*last_sale


class Market(object):

    def __init__(self, market):
        self.market = str(market)

    def write_daily_history(self):
        d = datetime.datetime.now()
        fileslug = self.market + '_summary_' + str(d) + '.txt'
        data = urlopen(
            'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=' + self.market + '&tickInterval=day').read().decode(
            'utf-8')
        parsed = json.loads(data)
        with open(fileslug, 'w') as f:
            json.dump(parsed, f, indent=4)

    def get_market_summary(self):
        print('THIS IS THE MARKET FUNCTION', self.market)
        url_slug = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market=' + self.market
        p = urlopen(url_slug).read()
        j = json.loads(p)
        data = j['result'][0]
        last_sale = float(data['Last'])
        day_high = data['High']
        day_low = data['Low']
        prev_day = float(data['PrevDay'])
        perror = (last_sale - prev_day) / prev_day * 100
        results = [last_sale, perror]
        return results








if __name__ == '__main__':
    # Market('BTC-NEO').write_daily_history()
    print(Market('BTC-NEO').get_market_summary())
    print(get_btc_summary())
