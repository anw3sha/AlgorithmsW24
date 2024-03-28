import numpy as np
import yfinance as yf
import pandas as pd
import talib as ta
import datetime
from enum import Enum


total_value = 0
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
        self.ticker = yf.Ticker(ticker.upper())
        self.shares = shares 
        self.balanced = False

        self.type = AssetType.EQUITY

        self.current_price = self.ticker.history(period="1d")['Close'][0]

        self.ratio_to_entire_portfolio = self.ticker.history(period="1d") * self.quantity / total_value
        self.avg_volume = self.ticker.info['averageVolume']
        
        self.fifty_two_week_high = self.ticker.info['fiftyTwoWeekHigh']
        self.fifty_two_week_low = self.ticker.info['fiftyTwoWeekLow']

        stock_data = yf.download(self.ticker, twentyStart, now, usecols=['Date', 'High', 'Low', 'Close'])
        self.avg_ATR_20 = ta.ATR(stock_data['High'], stock_data['Low'], stock_data['Close'], timeperiod=100)

        stock_data = yf.download(self.ticker, hundredStart, now, usecols=['Date', 'High', 'Low', 'Close'])
        self.avg_ATR_100 = ta.ATR(stock_data['High'], stock_data["Low"], stock_data["Close"], timeperiod=500)
        
        self.beta_SP = self.ticker.info['beta']


class Cash(Asset):
    def __init__(self, ticker, quantity):
        super().__init__(ticker, quantity)
        self.type = AssetType.CASH
