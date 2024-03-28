import numpy as np
import yfinance as yf
import pandas as pd
import talib as ta
import datetime
from enum import Enum


hundredStart = (datetime.datetime.now() - datetime.timedelta(days=700)).strftime("%Y-%m-%d")
twentyStart = (datetime.datetime.now() - datetime.timedelta(days=140)).strftime("%Y-%m-%d")
now = datetime.datetime.now().strftime("%Y-%m-%d")

class AssetType(Enum):
    EQUITY = "Equity"
    CASH = "Cash"

class Asset:
    def __init__(self, ticker, quantity):
        self.ticker = ticker
        self.quantity = quantity
    

class Equity(Asset):
    def __init__(self, ticker, shares):       
        super().__init__(ticker, shares) 
        self.tickerstr = ticker.upper()
        self.ticker = yf.Ticker(ticker.upper())
        self.shares = shares 
        self.balanced = False

        self.type = AssetType.EQUITY

        self.current_price = self.ticker.history(period="1d")['Close'].iloc[-1]
        self.ratio_to_entire_portfolio = -1.0
        #self.ratio_to_entire_portfolio = self.current_price * self.quantity / total_value

        self.avg_volume = self.ticker.info['averageVolume']
        
        self.fifty_two_week_high = self.ticker.info['fiftyTwoWeekHigh']
        self.fifty_two_week_low = self.ticker.info['fiftyTwoWeekLow']

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

        try:
          self.beta_SP = self.ticker.info['beta']
        except KeyError:
            self.beta_SP = None  # S

    
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


class Cash(Asset):
    def __init__(self, ticker, quantity):
        super().__init__(ticker, quantity)
        self.type = AssetType.CASH

    def print(self):
        print("Ticker: ", self.ticker)
        print("Quantity: ", self.quantity)