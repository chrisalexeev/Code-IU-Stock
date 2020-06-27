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
        self.curr_panel = 1
    
    def plot(self):
        mpf.plot(self.data, type='candle', volume=True, style='blueskies', main_panel=0, volume_panel=self.curr_panel, addplot=self.plots)
    
    def add_study(self, study):
        for plot in study.plots:
            # getting each data point for the plot
            points = np.zeros(len(self.data))
            for i in range(len(self.data)):
                points[i] = plot['function'](self.data.iloc, i)

            # making the actual plot
            plot_type = plot['type'] if 'type' in plot else 'line'
            color = plot['color'] if 'color' in plot else 'blue'
            if study.lower:
                self.plots.append(mpf.make_addplot(points, panel=self.curr_panel, type=plot_type, color=color))
            else:
                self.plots.append(mpf.make_addplot(points, panel=0, type=plot_type, color=color))
        if study.lower:
            self.curr_panel += 1
        print("study added")

    def addplot(self, data):
        self.plots.append(mpf.make_addplot(data))

    def __str__(self):
        return f"{self.ticker}"
