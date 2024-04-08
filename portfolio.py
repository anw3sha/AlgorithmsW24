from asset import *
import pandas as pd
from enum import Enum

class Portfolio:

  def __init__(self):
      self.assets = []
      self.total_value = 0

  # def read_portfolio(self, file_path):
  #     file = pd.read_csv(file_path)
  #     # read in type, ticker, shares, value
  #     # depending on type create a different object
  #     for row in file:
  #         if row[0] == 'Cash':
  #             cash = Cash(row['Ticker'], row['Shares'])
  #             self.assets.append(cash)
  #         else:
  #             equity = Equity(row['Ticker'], row['Shares'])
  #             self.assets.append(equity)
  #     return self.assets
      
  def read_portfolio(self, file_path):
    file = pd.read_csv(file_path)
    # read in type, ticker, shares, value
    # depending on type create a different object
    for index, row in file.iterrows():
        if row.iloc[0] == 'Cash':
            cash = Cash(row.iloc[0], row.iloc[1], row.iloc[2])
            self.assets.append(cash)
        else:
            equity = Equity(row.iloc[0], row.iloc[1], row.iloc[2])
            self.assets.append(equity)

    for asset in self.assets:
        if asset.classification == AssetType.CASH:
            self.total_value += asset.quantity
        else:
            self.total_value += asset.quantity * asset.ticker.history(period="1d")['Close'].iloc[-1]
          
    for asset in self.assets:
        if asset.classification == AssetType.CASH:
            asset.ratio_to_entire_portfolio = asset.quantity / self.total_value
        else:
            asset.ratio_to_entire_portfolio = asset.quantity * asset.ticker.history(period="1d")['Close'].iloc[-1] / self.total_value
    return self.assets

      
  def portfolio_size(self):
      for asset in self.assets:
        if asset.classification == AssetType.CASH:
          self.total_value += asset.quantity
        else:
          self.total_value += asset.quantity * asset.ticker.history(period="1d")
      return self.total_value

  def get_portfolio(self):
      return self.assets

  def print_portfolio(self):
      for asset in self.assets:
          asset.print()
          print("\n")
          
  def print_to_csv(self, filename):
      with open(filename, 'w', newline='') as file:
          writer = csv.writer(file)
          writer.writerow(["Ticker", "Shares", "Current Price", "Ratio to entire portfolio", "Beta SP"])
      for asset in self.assets:
          asset.to_csv(filename)

  def fix_ratios(self):
    for asset in self.assets:
      if asset.classification == AssetType.CASH:
          asset.ratio_to_entire_portfolio = asset.quantity / self.total_value
      else:
          asset.ratio_to_entire_portfolio = asset.quantity * asset.ticker.history(period="1d")['Close'].iloc[-1] / self.total_value
      
  def updateMarkets(self):
      self.total_value = 0
      for asset in self.assets:
          asset.updateMarkets()
      
      self.total_value = self.portfolio_size()
      self.fix_ratios()

     
  def buy(self, ticker, quantity):
    if ticker == 'CASH':
        self.assets[0].quantity += quantity
        self.updateMarkets()
    else: 
      for asset in self.assets:
        if asset.ticker == ticker:
          asset.quantity += quantity
          self.assets[0].quantity -= asset.current_price * quantity # update cash
          self.updateMarkets()
          return
        else: 
           equity = Equity(ticker, quantity)
           self.assets.append(equity)
           self.assets[0].quantity -= asset.current_price * quantity # update cash
           self.updateMarkets()
           return
  
  def sell(self, ticker, quantity):
    for asset in self.assets:
      if asset.ticker == ticker:
        asset.quantity -= quantity
        self.assets[0].quantity += asset.current_price * quantity # update cash
        if asset.quantity == 0:
          self.assets.remove(asset)
          # update cash
      else:
          print("Asset not found")
    self.updateMarkets()

    def rebalance():
      self.updateMarkets()
       
      # accept a csv file with the new ratios, then rebalance the portfolio and update markets
      # buy and sell according to intented ratios
