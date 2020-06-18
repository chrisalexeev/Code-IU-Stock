import pandas as pd
import mplfinance as mpf
from datetime import date
from Study import MovingAverage
import numpy as np

class Stock:
    def __init__(self,ticker,filename):
        self.ticker = ticker
        self.plots = []
        self.data = pd.read_csv(filename, index_col=0, parse_dates=True)
    
    def plot(self):
        mpf.plot(self.data, type='candle', volume=True, style='yahoo', addplot=self.plots)
    
    def add_study(self, study):
        print("adding a study...")
        points = np.zeros(len(self.data))
        for i in range(len(self.data)):
            # points.append(study.get_point(self.data.iloc, i))
            points[i] = study.get_point(self.data.iloc, i)
        print("making it a plot...")
        self.plots.append(mpf.make_addplot(points))
        print("study added")

    def addplot(self, data):
        self.plots.append(mpf.make_addplot(data))

    def __str__(self):
        return f"{self.ticker}"
