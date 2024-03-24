class stock:
  ticker = asdfasdf
  avg_+volume
  SD of volume
  52 week hiogh/low
  ratio to entire portofolio
  Beta with respect to 
  avg ATR 20 week 100 week
  ### run smA on ATR to find covergence


array of stocks []

class AssetAllocation:
   

def (Ass, arr):
  balance = False
  while (!balanced):
    for i in arr:
      fix with respect to Ass




from scipy.optimize import minimize
import numpy as np
import pandas as pd

returns = df

mean_returns = returns.mean()
cov_matrix = returns.cov()
mean_atr = reutrns['atr'].mean()


# Number of asset classes
num_assets = len(mean_returns)

# Portfolio optimization function
def portfolio_volatility(weights, mean_returns, cov_matrix):
    return np.sqrt(np.dot(np.dot(mean_atr.T, np.dot(cov_matrix, weights))weights.T))

# Constraints: weights sum to 1
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# Bounds for each weight
bounds = tuple((0, 1) for asset in range(num_assets))

# Initial guess (equal distribution)
initial_guess = num_assets * [1. / num_assets,]

# Minimize portfolio volatility
optimal_weights = minimize(portfolio_volatility, initial_guess, args=(mean_returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

print("Optimal weights:", optimal_weights.x)