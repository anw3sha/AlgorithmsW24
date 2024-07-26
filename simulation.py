import numpy as np
import pandas as pd
from portfolio import Portfolio
from asset import AssetType, Equity, Cash
import random

class PortfolioSimulation:
    def __init__(self, portfolio, num_simulations=1000, num_days=252):
        self.portfolio = portfolio
        self.num_simulations = num_simulations
        self.num_days = num_days
        self.best_portfolio = None
        self.best_portfolio_value = -np.inf
        self.original_portfolio_value = self.calculate_portfolio_value(self.portfolio.assets)

    def calculate_portfolio_value(self, assets):
        return sum(asset.quantity * asset.current_price for asset in assets if asset.classification != AssetType.CASH)

    def simulate_portfolio(self):
        results = np.zeros(self.num_simulations)
        for i in range(self.num_simulations):
            final_value = self.run_simulation()
            results[i] = final_value
            if final_value > self.best_portfolio_value:
                self.best_portfolio_value = final_value
                self.best_portfolio = self.save_portfolio()
        return results

    def run_simulation(self):
        total_budget = self.original_portfolio_value
        
        for asset in self.portfolio.assets:
            if asset.classification == AssetType.CASH:
                continue
            max_quantity = int(total_budget / asset.current_price)
            asset.quantity = random.randint(0, max_quantity)
            total_budget -= asset.quantity * asset.current_price
            if total_budget <= 0:
                break

        daily_returns = pd.DataFrame(index=range(self.num_days), columns=[asset.tickerstr for asset in self.portfolio.assets if asset.classification != AssetType.CASH])

        for asset in self.portfolio.assets:
            if asset.classification == AssetType.CASH:
                continue
            mu = asset.returns.mean()
            sigma = asset.returns.std()
            random_returns = np.random.normal(mu, sigma, self.num_days)
            daily_returns[asset.tickerstr] = random_returns

        portfolio_values = np.zeros(self.num_days)
        portfolio_values[0] = self.calculate_portfolio_value(self.portfolio.assets)  # This correctly sets initial portfolio value to the scenario basis
        for day in range(1, self.num_days):
            daily_return = daily_returns.iloc[day].mean()
            portfolio_values[day] = portfolio_values[day-1] * (1 + daily_return)

        final_portfolio_value = portfolio_values[-1]
        return final_portfolio_value

    def save_portfolio(self):
        # Return a copy of the portfolio with current best configuration.
        return [self.deep_copy_asset(asset) for asset in self.portfolio.assets]

    def deep_copy_asset(self, asset):
        if asset.classification == AssetType.CASH:
            return Cash(asset.type, asset.ticker, asset.quantity)
        else:
            copied_equity = Equity(asset.type, asset.tickerstr, asset.quantity)
            copied_equity.current_price = asset.current_price
            copied_equity.industry = asset.industry
            copied_equity.ratio_to_entire_portfolio = asset.ratio_to_entire_portfolio
            copied_equity.shares = asset.shares
            copied_equity.avg_volume = asset.avg_volume
            copied_equity.fifty_two_week_high = asset.fifty_two_week_high
            copied_equity.fifty_two_week_low = asset.fifty_two_week_low
            copied_equity.beta_SP = asset.beta_SP
            copied_equity.returns = asset.returns.copy()
            return copied_equity

if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.read_portfolio('portfolio.csv')
    num_simulations = 1000
    simulator = PortfolioSimulation(portfolio, num_simulations)
    simulation_results = simulator.simulate_portfolio()

    original_portfolio_value = simulator.original_portfolio_value
    optimal_portfolio_value = simulator.calculate_portfolio_value(simulator.best_portfolio)
    
    print(f"\nOriginal Portfolio Value: ${original_portfolio_value:.2f}")

    print(f"\nInitial Value of Best Portfolio: ${optimal_portfolio_value:.2f}")
    print(f"Final Value of Best Portfolio: ${simulator.best_portfolio_value:.2f}")

    original_portfolio_assets = portfolio.assets
    print("\nOriginal Portfolio Configuration:")
    for asset in original_portfolio_assets:
        if asset.classification == AssetType.CASH:
            print(f"Cash: ${asset.quantity:.2f}")
        else:
            print(f"{asset.tickerstr}: {asset.quantity:.2f} shares")

    best_portfolio_assets = simulator.best_portfolio
    print("\nBest Portfolio Configuration:")
    for asset in best_portfolio_assets:
        if asset.classification == AssetType.CASH:
            print(f"Cash: ${asset.quantity:.2f}")
        else:
            print(f"{asset.tickerstr}: {asset.quantity:.2f} shares")