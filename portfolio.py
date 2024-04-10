from asset import *
import pandas as pd
from enum import Enum

class Portfolio:


  def __init__(self):
      self.assets = []
      self.total_value = 0
      self.riskFreeRate = yf.download('^TNX', period="1d")['Close'].iloc[-1]

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
          writer.writerow(["Ticker", "Industry", "Shares", "Current Price", "Ratio to entire portfolio", "Beta SP"])
      for asset in self.assets:
          asset.to_csv(filename)

  def fix_ratios(self):
    for asset in self.assets:
      if asset.classification == AssetType.CASH:
          asset.ratio_to_entire_portfolio = asset.quantity / self.total_value
      else:
          asset.ratio_to_entire_portfolio = asset.quantity * asset.ticker.history(period="1d")['Close'].iloc[-1] / self.total_value
  
  def calculate_industry_ratios(self):
    # Initialize a dictionary to store the total ratio for each industry
    industry_ratios = {}

    for asset in self.assets:
        # If the asset's industry is not in the dictionary, add it with the asset's ratio
        if asset.industry not in industry_ratios:
            industry_ratios[asset.industry] = asset.ratio_to_entire_portfolio
        # If the asset's industry is in the dictionary, add the asset's ratio to the total
        else:
            industry_ratios[asset.industry] += asset.ratio_to_entire_portfolio

    return industry_ratios

  def updateMarkets(self):
      self.total_value = 0
      for asset in self.assets:
          asset.updateMarkets()
      
      self.total_value = self.portfolio_size()
      self.fix_ratios()
      self.riskFreeRate = yf.download('^TNX', period="1d")['Close'].iloc[-1]

  def print_industries(self):
    for asset in self.assets[1:]:  
        print(asset.industry)
        print("\n")
     
  def buy(self, ticker, quantity):
    if ticker == 'CASH':
        self.assets[0].quantity += quantity
        self.updateMarkets()
    else: 
        for asset in self.assets:
            if asset.ticker == ticker:
                purchase_amount = asset.current_price * quantity
                if self.assets[0].quantity - purchase_amount < 0:  # Check if the purchase would result in negative cash
                    print("Insufficient cash to buy this quantity of asset.")
                    return
                asset.quantity += quantity
                self.assets[0].quantity -= purchase_amount  # update cash
                self.updateMarkets()
                return
            else: 
                equity = Equity(ticker, quantity)
                purchase_amount = equity.current_price * quantity
                if self.assets[0].quantity - purchase_amount < 0:  # Check if the purchase would result in negative cash
                    print("Insufficient cash to buy this quantity of asset.")
                    return
                self.assets.append(equity)
                self.assets[0].quantity -= purchase_amount  # update cash
                self.updateMarkets()
                return
  
  def calcSharpe(self):
    

  def sell(self, ticker, quantity):
    for asset in self.assets:
        if asset.ticker == ticker:
            sale_amount = asset.current_price * quantity
            asset.quantity -= quantity
            self.assets[0].quantity += sale_amount  # update cash
            if asset.quantity == 0:
                self.assets.remove(asset)
        else:
            print("Asset not found")
    self.updateMarkets()

  def rebalance(self, csv_file):
    # read the target ratios from a CSV file
    target_ratios_df = pd.read_csv(csv_file)
    target_ratios = dict(zip(target_ratios_df['industry'], target_ratios_df['target percentage']))

    # calculate the current industry ratios
    current_ratios = self.calculate_industry_ratios()

    tolerance = 0.05  # adjust this value as needed
    balanced = False

    while not balanced:
      balanced = True

      for industry, current_ratio in current_ratios.items():
        target_ratio = target_ratios.get(industry, 0)

        if abs(current_ratio - target_ratio) > tolerance:
          balanced = False
          # find the assets in this industry, starting from the second asset
          assets_in_industry = [asset for asset in self.assets[1:] if asset.industry == industry]
          for asset in assets_in_industry:
            if current_ratio > target_ratio:
              asset.sell(asset.ticker, 1) # sell one share
            else:
              asset.buy(asset.ticker, 1) # buy one share

    self.updateMarkets()
    current_ratios = self.calculate_industry_ratios()
       
      # Consumer Cyclical, Industrials, ETF, Fixed Income, Communication Services, Financial Services, Healthcare, Technology