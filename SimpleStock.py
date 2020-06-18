import pandas as pd
import mplfinance as mpf

class Stock:
    def __init__(self,ticker,filename):
        self.ticker = ticker
        self.plots = []
        self.data = pd.read_csv(filename, index_col=0, parse_dates=True)
    
    def plot(self):
        mpf.plot(self.data, type='candle', volume=True, style='yahoo', addplot=self.plots)

    def addplot(self, data):
        self.plots.append(mpf.make_addplot(data))

    def __str__(self):
        return f"{self.ticker}"

if __name__ == "__main__":
    baba = Stock("BABA", "BABA.csv")
    baba.plot()
