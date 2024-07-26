import numpy as np
import pandas as pd
from portfolio import Portfolio
from asset import AssetType, Equity, Cash

class PortfolioSimulation:
    def __init__(self, portfolio, num_simulations=1000, num_days=252):
        self.portfolio = portfolio
        self.num_simulations = num_simulations
        self.num_days = num_days
        self.best_portfolio = None
        self.best_sharpe_ratio = -np.inf
        self.original_portfolio_value = self.calculate_portfolio_value(self.portfolio.assets)
        
    def calculate_portfolio_value(self, assets):
        return sum(asset.quantity * asset.current_price for asset in assets if asset.classification != AssetType.CASH)

    def simulate_portfolio(self):
        results = np.zeros(self.num_simulations)
        for i in range(self.num_simulations):
            sharpe_ratio = self.run_simulation()
            results[i] = sharpe_ratio
            if sharpe_ratio > self.best_sharpe_ratio:
                self.best_sharpe_ratio = sharpe_ratio
                self.best_portfolio = self.save_portfolio()
        return results

    def run_simulation(self):
        # Simulate daily returns for each asset
        daily_returns = pd.DataFrame(index=range(self.num_days), columns=[asset.tickerstr for asset in self.portfolio.assets if asset.classification != AssetType.CASH])
        
        for asset in self.portfolio.assets:
            if asset.classification == AssetType.CASH:
                continue
            mu = asset.returns.mean()
            sigma = asset.returns.std()
            random_returns = np.random.normal(mu, sigma, self.num_days)
            daily_returns[asset.tickerstr] = random_returns

        # Calculate portfolio value over time
        portfolio_values = np.zeros(self.num_days)
        portfolio_values[0] = self.portfolio.total_value
        for day in range(1, self.num_days):
            daily_return = daily_returns.iloc[day].mean()
            portfolio_values[day] = portfolio_values[day-1] * (1 + daily_return)

        # Final portfolio value
        final_portfolio_value = portfolio_values[-1]

        # Calculate Sharpe Ratio
        annualized_return = (portfolio_values[-1] / portfolio_values[0]) ** (252 / self.num_days) - 1
        portfolio_std_dev = daily_returns.mean(axis=1).std() * np.sqrt(252)
        risk_free_rate = self.portfolio.riskFreeRate / 100
        sharpe_ratio = (annualized_return - risk_free_rate) / portfolio_std_dev

        return sharpe_ratio

    def save_portfolio(self):
        # Create a deep copy of the portfolio assets to avoid mutations during simulations
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
            copied_equity.returns = asset.returns.copy()  # Ensure deep copy of returns
            return copied_equity
            
if __name__ == "__main__":
    portfolio = Portfolio()
    portfolio.read_portfolio('portfolio.csv')
    num_simulations = 1000
    simulator = PortfolioSimulation(portfolio, num_simulations)
    simulation_results = simulator.simulate_portfolio()

    worst_sharpe_ratio = np.min(simulation_results)

    print("Best Sharpe Ratio:", simulator.best_sharpe_ratio)
    print("Worst Sharpe Ratio:", worst_sharpe_ratio)

    # Calculate and print the value of the original portfolio
    original_portfolio_value = simulator.original_portfolio_value
    print(f"\nOriginal Portfolio Value: ${original_portfolio_value:.2f}")

    # Calculate and print the value of the optimal portfolio
    optimal_portfolio_value = simulator.calculate_portfolio_value(simulator.best_portfolio)
    print(f"Optimal Portfolio Value: ${optimal_portfolio_value:.2f}")

    # Print the best portfolio configuration
    best_portfolio_assets = simulator.best_portfolio
    print("\nBest Portfolio Configuration:")
    for asset in best_portfolio_assets:
        if asset.classification == AssetType.CASH:
            print(f"Cash: ${asset.quantity:.2f}")
        else:
            print(f"{asset.tickerstr}: {asset.quantity:.2f} shares")
