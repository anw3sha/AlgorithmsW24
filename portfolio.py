from asset import *
import pandas as pd
from enum import Enum

class Portfolio:

  def __init__(self):
      self.assets = []
      self.total_value = 0

  def read_portfolio(self, file_path):
      file = pd.read_csv(file_path)
      # read in type, ticker, shares, value
      # depending on type create a different object
      for row in file:
          if row['type'] == 'Cash':
              cash = Cash(row['ticker'], row['shares'])
              self.assets.append(cash)
          else:
              equity = Equity(row['ticker'], row['shares'])
              self.assets.append(equity)
      return self.assets
      
  def portfolio_size(self):
      for asset in self.assets:
        if asset.type == AssetType.CASH:
          self.total_value += asset.quantity
        else:
          self.total_value += asset.quantity * asset.ticker.history(period="1d")
      return self.total_value

  def get_portfolio(self):
      return self.assets