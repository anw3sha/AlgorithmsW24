import numpy as np
import yfinance as yf
import pandas as pd
import talib as ta
import datetime
from enum import Enum
import csv


hundredStart = (datetime.datetime.now() - datetime.timedelta(days=700)).strftime("%Y-%m-%d")
twentyStart = (datetime.datetime.now() - datetime.timedelta(days=140)).strftime("%Y-%m-%d")
now = datetime.datetime.now().strftime("%Y-%m-%d")

class AssetType(Enum):
    EQUITY = "Equity"
    CASH = "Cash"

class Asset:
    def __init__(self, type, ticker, quantity):
        self.type = type
        self.ticker = ticker
        self.quantity = quantity

class Equity(Asset):
    def __init__(self, type, ticker, shares):  
        super().__init__(type, ticker, shares) 
        self.classification = AssetType.EQUITY
        self.tickerstr = ticker.upper()
        self.ticker = yf.Ticker(ticker.upper())
        self.shares = int(shares)
        self.balanced = False #todo don't forget about this

        self.equityType = None

        self.current_price = self.ticker.history(period="1d")['Close'].iloc[-1]
        self.ratio_to_entire_portfolio = -1.0

        self.avg_volume = self.ticker.info['averageVolume']
        
        self.fifty_two_week_high = self.ticker.info['fiftyTwoWeekHigh']
        self.fifty_two_week_low = self.ticker.info['fiftyTwoWeekLow']

        try:
          self.beta_SP = self.ticker.info['beta']
        except KeyError:
            self.beta_SP = None  
        
    def updateMarkets(self):
        self.current_price = self.ticker.history(period="1d")['Close'].iloc[-1]
        self.avg_volume = self.ticker.info['averageVolume']
        self.fifty_two_week_high = self.ticker.info['fiftyTwoWeekHigh']
        self.fifty_two_week_low = self.ticker.info['fiftyTwoWeekLow']
        try:
          self.beta_SP = self.ticker.info['beta']
        except KeyError:
            self.beta_SP = None
    
    
    def print (self):
        print("Ticker: ", self.tickerstr)
        print("Shares: ", self.shares)
        print("Current Price: ", self.current_price)
        print("Ratio to entire portfolio: ", self.ratio_to_entire_portfolio)
        print("Average Volume: ", self.avg_volume)
        print("52 Week High: ", self.fifty_two_week_high)
        print("52 Week Low: ", self.fifty_two_week_low)
        # print("Average ATR 20: ", self.avg_ATR_20)
        # print("Average ATR 100: ", self.avg_ATR_100)
        print("Beta SP: ", self.beta_SP)

    def to_csv(self, filename):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.type, self.tickerstr, self.shares, self.current_price, self.ratio_to_entire_portfolio, self.beta_SP])


class Cash(Asset):
    def __init__(self, type, ticker, quantity):
        super().__init__(type, ticker, quantity)
        self.shares = 1       
        self.ratio_to_entire_portfolio = -1.0
        self.classification = AssetType.CASH

    def print(self):
        print("Ticker: ", self.ticker)
        print("Shares: ", self.shares)
        print("Quantity: ", self.quantity)
        print("Ratio to entire portfolio: ", self.ratio_to_entire_portfolio)
    
    def to_csv(self, filename):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.type, self.ticker, self.shares, self.quantity, self.ratio_to_entire_portfolio, " "])
    
    def updateMarkets(self):
        pass


# old code for constructor
        # stock_data = yf.download(tickerstr, start=twentyStart, end=now, progress=False)
        # stock_data = stock_data[['High', 'Low', 'Close']].copy()
        # stock_data['ATR'] = ta.ATR(stock_data['High'], stock_data['Low'], stock_data['Close'], timeperiod=1)
        # self.avg_ATR_20 = stock_data['ATR'].rolling(window=100).mean().iloc[-1]

        # self.avg_ATR_20 = ta.ATR(stock_data['High'], stock_data['Low'], stock_data['Close'], timeperiod=100)

        # stock_data = yf.download(tickerstr, start = hundredStart, end = now, progress = False)
        # stock_data = stock_data[['High', 'Low', 'Close']].copy()
        # stock_data['ATR'] = ta.ATR(stock_data['High'], stock_data['Low'], stock_data['Close'], timeperiod=1)
        # self.avg_ATR_100 = stock_data['ATR'].rolling(window=500).mean().iloc[-1]
        #self.beta_SP = self.ticker.info['beta']


        # if equityType == "Stock":
        #     self.equityType = EquityType.STOCK
        # elif equityType == "ETF":
        #     self.equityType = EquityType.ETF
        # elif equityType == "Index":
        #     self.equityType = EquityType.INDEX
        # elif equityType == "Fixed Income":
        #     self.equityType = EquityType.FIXED_INCOME
        # else :
        #     print("Invalid equity type")
        #     self.equityType = None
        
        # class EquityType(Enum):
        #     STOCK = "Stock"
        #     ETF = "ETF"
        #     INDEX = "Index"
        #     FIXED_INCOME = "Fixed Income"