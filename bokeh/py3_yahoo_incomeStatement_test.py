from yahoofinancials import YahooFinancials
import pandas as pd
import json
import pprint
import json

yahoo_financials = YahooFinancials('GOOG')
#json_object = yahoo_financials.get_financial_stmts('annual', 'balance')
#json_object = yahoo_financials.get_financial_stmts('quarterly', 'cash')
#json_object = yahoo_financials.get_financial_stmts('quarterly', 'income')
json_object = yahoo_financials.get_key_statistics_data()

print(json.dumps(json_object, indent=1))
'''
if __name__=="__main__":
    stock_symbol = 'FB'
    get_yahooFinancials(stock_symbol)
    '''