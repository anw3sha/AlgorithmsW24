from portfolio import Portfolio
import random
from asset import *

#update function
#print everything
#buy function and sell function and rebalace it based on that
#portfolio class with dictionary of stocks

p = Portfolio()
p.read_portfolio('portfolio.csv')
temp = p
# p.print_portfolio()
# p.print_to_csv('output.csv')
# in.p.print_industries()
# p.rebalance('target_ratios.csv')

total_equity_value = 0
for equity in p.assets:
    if equity.classification == AssetType.CASH: 
          continue
    
    total_equity_value += equity.shares
    
curr_final_sharp = temp.calcSharpe()
curr_final_portfolio = temp


for k in range(0, 100):
    
    temp_total_equity = total_equity_value
    new_temp = p

    for i in range(0, len(new_temp.assets) - 1):
        random_int = random.randint(0, min(80, temp_total_equity))
        new_temp.assets[i].shares = random_int
        temp_total_equity -= random_int
        #print(new_temp.assets[i].shares)

    new_temp.assets[len(new_temp.assets) - 1].shares = temp_total_equity

    sharp = new_temp.calcSharpe()

    if (sharp > curr_final_sharp):
        curr_final_sharp = sharp
        curr_final_portfolio = new_temp

    
print(f"Final Sharpe: {curr_final_sharp}")
total = 0

for equity in curr_final_portfolio.assets:
    if equity.classification == AssetType.CASH: 
          continue
    print(f"{equity.tickerstr}: {equity.shares}")
    total += equity.shares

print(total)



