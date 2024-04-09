import yfinance as yf

msft = yf.Ticker("SGOV")

info = msft.info

for key in info:
    print(key, info[key])
