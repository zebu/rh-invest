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

def login(args=''):
    global isLoggedIn
    if (not isLoggedIn):
        print('Logging into robinhood')
        if (not os.path.exists(config['credentialsPath'])):
            raise Exception("No credentials exist. Please create them")
        credentials=readJSON(config['credentialsPath'])
        isLoggedIn = rh.login(credentials['username'],credentials['password'])

def showInvestments(args):
    print("showInvestments")
    for item in readJSON(config['investmentsPath']):
        print(item['symbol'])

def readTrueFalse(prompt):
    while True:
        result = input(prompt)
        if (result.lower() in ['y','yes','true']):
            return True
        if (result.lower() in ['n','no','false']):
            return False

# I can't decide. Do I want to mannage investments via watchlists on rh or in a local file?
# If via watch list, you'd have to add a new stock to the list prior to investing
#  you'd still have to keep a local file if you wanted to weight some securities over others
# For now I think it's better to manage everything in a local file
def buyInvestments(args):
    print(f'buyInvestments')
    login()

    investments=readJSON(config['investmentsPath'])
    symbols = []
    for item in investments:
        symbols.append(item['symbol'])

    current_prices = rh.get_latest_price(symbols)
    spread=math.floor(args.amount/len(investments)) #equally divided for now

    plan=[]
    for security in investments:
        symbol=security['symbol']
        price=float(current_prices.pop(0))
        quantity=price/spread
        plan.append({'symbol':symbol, 'quantity':quantity})

    for security in plan:
        print(f"buy symbol: {security['symbol']:>4s} quantity: {security['quantity']:13.8f}")
        
    if (args.dryrun):
        print('Dryrun. No action taken')
        return
        
    if (readTrueFalse('execute trade (y/n)?')):
        for security in plan:
            print(f"executed {security['symbol']:>4s} quantity: {security['quantity']:13.8f}")
    else:
        print('No action taken')

def showPositions(args):
    print("showPositions")
    login()

    positions_data = rh.get_open_stock_positions()
    for item in positions_data:
        #print(item)
        print(f"symbol: {rh.get_symbol_by_url(item['instrument']):>4s} quanity: {float(item['quantity']):13.8f} cost: {float(item['quantity'])*float(item['average_buy_price']):13.8f}")


# Notes
# Credentials needs to be created first
# inventments.json holds the list of all securities and crypto being traded
#
# 
# TODO
# The dollar amoount is equally divided across all securities. Need to implement weighting
# Implement crypto    

# command scratch pad
#invest credentials
#invest show (not liking this name)
#invest positions
#invest buy 1000 --dryrun --symbol (list)
#invest add AAPL (need weighting and type)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='rhinvest')
    subparsers = parser.add_subparsers()
    
    parser_login = subparsers.add_parser('login', help='login to robinhood')
    parser_login.set_defaults(func=login)

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



