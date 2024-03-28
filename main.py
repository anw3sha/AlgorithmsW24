from portfolio import *

#update function
#print everything
#buy function and sell function and rebalace it based on that
#portfolio class with dictionary of stocks

def main():
    p = Portfolio()
    p.read_portfolio("portfolio.csv")
    print(p.get_portfolio())
    print(p.portfolio_size())

