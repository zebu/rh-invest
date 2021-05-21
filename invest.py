import robin_stocks.robinhood as rh
import argparse, json, os, getpass, sys, math

config = { 'investmentsPath':'investments.json', 'credentialsPath':'credentials.json'}
isLoggedIn = None

class Stock(object):
    def __init__(self, symbol, weight):
        self.symbol = symbol
        self.weight = weight

class Crypto(object):
    def __init__(self, symbol, weight):
        self.symbol = symbol
        self.weight = weight
  
def readJSON(fpath):
    with open(fpath, 'r') as input:
        return json.load(input)

def writeJSON(fpath, obj):
    with open(fpath, 'w') as output:
        json.dump(obj, output, indent=4, sort_keys=True, default=lambda x: x.__dict__)

def updateCredentials(args):
    print("updateCredentials")

    credentials={}
    if (os.path.exists(config['credentialsPath'])):
        credentials=readJSON(config['credentialsPath'])
    
    # assuming I have a tty
    username_prompt='Username:'
    if ('username' in credentials):
        username_prompt=f"Username ({credentials['username']}):"

    while True:
        username = input(username_prompt)
        if (not username and 'username' in credentials):
            username=credentials['username']

        if (username):
            credentials['username'] = username
            break

    while True:
        password = getpass.getpass("Password: ")
        if (password):
            credentials['password'] = password
            break

    writeJSON(config['credentialsPath'], credentials)

    print('credentials updated')

def login():
    global isLoggedIn
    if (not isLoggedIn):
        print('Logging into robinhood')
        if (not os.path.exists(config['credentialsPath'])):
            raise Exception("No credentials exist. Please create them")
        credentials=readJSON(config['credentialsPath'])
        loginx = rh.login(credentials['username'],'password')

def showInvestments(args):
    print("showInvestments")
    for item in readJSON(config['investmentsPath']):
        print(item['symbol'])

def buyInvestments(args):
    print("buyInvestments")
    login()

    investments=readJSON(config['investmentsPath'])
    symbols = []
    for item in investments:
        symbols.append(item['symbol'])

    #item['pending_average_buy_price']/
    spread=math.floor(args.amount/len(investments))
    #print(spread)

    #current_prices = rh.get_latest_price(symbols)
    #print(current_prices)
    for item in investments:
        symbol=item['symbol']

        #I don't like all of the rest calls. maybe use rh.get_latest_price(symbols)
        quanity=float(rh.get_latest_price(item['symbol']).pop())/spread
        print(f"buy symbol: {symbol:>4s} quanity: {quanity:13.8f}")
        #rh.order_buy_market('AAPL',10)
        #print('buy '+item['symbol']+' ')

def showPositions(args):
    print("showPositions")
    login()

    positions_data = rh.get_open_stock_positions()
    for item in positions_data:
        #print(item)
        print(f"symbol: {rh.get_symbol_by_url(item['instrument']):>4s} quanity: {float(item['quantity']):13.8f} cost: {float(item['quantity'])*float(item['average_buy_price']):13.8f}")
        
# investments is a json file containing stock or crypto objects


#stocks_dir='stocks'

#stocks_path='fool.pk1'
#stock_list = [Stock('TTC', 'stock', 100),Stock('ABNB', 'stock', 100),Stock('IDXX', 'stock', 100),Stock('MTN', 'stock', 100),Stock('OKTA', 'stock', 100),Stock('UNP', 'stock', 100),Stock('TTD', 'stock', 100),Stock('TEAM', 'stock', 100),Stock('SHOP', 'stock', 100),Stock('FVRR', 'stock', 100),Stock('CRWD', 'stock', 100)]
#stocks = loadStocks(stocks_path)
#for item in stocks:
#    print(item.ticker)

#login = rh.login()
#positions_data = rh.get_watchlist_by_name(name='Fool')
#print(positions_data)
#for item in positions_data['results']:
#    print(item['symbol'])

#invest buy 1000 --dryrun --ticker
#invest add AAPL

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='rhinvest')
    subparsers = parser.add_subparsers()
    
    parser_credentials = subparsers.add_parser('credentials', help='create or update stored credentials')
    parser_credentials.set_defaults(func=updateCredentials)

    parser_show = subparsers.add_parser('show', help='show the current investments')
    parser_show.set_defaults(func=showInvestments)

    parser_show = subparsers.add_parser('positions', help='show the current positions')
    parser_show.set_defaults(func=showPositions)

    parser_buy = subparsers.add_parser('buy', help='buy from the current investments')
    parser_buy.set_defaults(func=buyInvestments)
    parser_buy.add_argument('amount', type=int, help='The amount of money in dollars you want to invest')
    parser_buy.add_argument('--dryrun', action='store_true', help='do not perform any actions')


    args = parser.parse_args()
    args.func(args)



