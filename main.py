from portfolio import Portfolio

#update function
#print everything
#buy function and sell function and rebalace it based on that
#portfolio class with dictionary of stocks

p = Portfolio()
p.read_portfolio('portfolio.csv')
# p.print_portfolio()
# p.print_to_csv('output.csv')
p.print_industries()
# p.rebalance('target_ratios.csv')