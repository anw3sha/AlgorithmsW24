import numpy as np
import pandas as pd
import yfinance as yf

class stock:
  ticker = ""
  avg_volume = 0
  fifty_two_week_high = 0
  fifty_two_week_low = 0
  ratio_to_entire_portfolio = 0.0
  beta_SP = 0.0
  avg_ATR_20 = 0.0
  avg_ATR_100 = 0.0

