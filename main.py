from portfolio import Portfolio
import random
from asset import *


def Rebalance_main(target, p):
    for i in range(0, len(target.assets)):
        if target.assets[i].classification == AssetType.CASH: 
            continue

        difference = target.assets[i].shares - p.assets[i].shares

        #print(difference)

        if difference > 0:
            print(f"Buy {abs(difference)} shares of {target.assets[i].tickerstr}")
        elif difference < 0:
            print(f"Sell {abs(difference)} shares of {target.assets[i].tickerstr}")

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

curr = Portfolio()
curr.read_portfolio('portfolio.csv')

Rebalance_main(curr_final_portfolio, curr)




"""
Final Sharpe: 2.583967902009879
MTN: 4
GNRC: 29
SPMD: 53
SGOV: 27
META: 52
VIRT: 67
VRTX: 37
PERI: 37
CSV: 23
AX: 4
GTX: 0
ENPH: 4
Total Equity Assets: 337
"""