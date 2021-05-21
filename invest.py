#import robin_stocks.robinhood as rh
import argparse, json, os, getpass, sys

config = { 'investmentsPath':'investments.json', 'credentialsPath':'credentials.json'}

class Stock(object):
    def __init__(self, ticker, weight):
        self.ticker = ticker
        self.weight = weight

class Crypto(object):
    def __init__(self, ticker, weight):
        self.ticker = ticker
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

def showInvestments(args):
    print("showInvestments")
    for item in readJSON(config['investmentsPath']):
        print(item['ticker'])

def buyInvestments(args):
    print("buyInvestments")

    investments=readJSON(config['investmentsPath'])
    spread=args.amount/len(investments)
    print(spread)
    for item in investments:
        print('buy '+item['ticker']+' ')

# investments is a json file containing stock or crypto objects

#print("Loading investments "+fpath)
#print("Writing stock information "+fpath)

# read login/password

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

    parser_show = subparsers.add_parser('buy', help='buy from the current investments')
    parser_show.set_defaults(func=buyInvestments)
    parser_show.add_argument('amount', type=int, help='The amount of money in dollars you want to invest')
    parser_show.add_argument('--dryrun', action='store_true', help='do not perform any actions')

    args = parser.parse_args()
    args.func(args)



