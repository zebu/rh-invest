import robin_stocks.robinhood as rh
import json

class Stock(object):
    def __init__(self, ticker, type, weight):
        self.ticker = ticker
        self.type = type
        self.weight = weight

def loadStocks(fpath):
    print("Loading stock information "+fpath)

    with open(fpath, 'r') as input:
        return json.load(input)

def writeStocks(fpath, stock_list):
    print("Writing stock information "+fpath)

    with open(fpath, 'w') as output:
        json.dump(stock_list, output, indent=4, sort_keys=True, default=lambda x: x.__dict__)

def 
stocks_dir='stocks'

stocks_path='fool.pk1'
stock_list = [Stock('TTC', 'stock', 100),Stock('ABNB', 'stock', 100),Stock('IDXX', 'stock', 100),Stock('MTN', 'stock', 100),Stock('OKTA', 'stock', 100),Stock('UNP', 'stock', 100),Stock('TTD', 'stock', 100),Stock('TEAM', 'stock', 100),Stock('SHOP', 'stock', 100),Stock('FVRR', 'stock', 100),Stock('CRWD', 'stock', 100)]
writeStocks(stocks_path, stock_list)
#stocks = loadStocks(stocks_path)
#for item in stocks:
#    print(item.ticker)

#login = rh.login()
#positions_data = rh.get_watchlist_by_name(name='Fool')
#print(positions_data)
#for item in positions_data['results']:
#    print(item['symbol'])






