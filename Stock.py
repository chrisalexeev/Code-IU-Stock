import pandas as pd
import mplfinance as mpf
from datetime import date
from Study import MovingAverage
import numpy as np
from Data import Data

class Stock:
    def __init__(self,ticker,filename):
        self.ticker = ticker
        self.plots = []
        self.candles = pd.read_csv(filename, index_col=0, parse_dates=True)
        self.data = Data(self.candles.reset_index().to_dict(orient='list'))
        self.curr_panel = 1
    
    def plot(self):
        mpf.plot(self.candles, type='candle', volume=True, style='blueskies', main_panel=0, volume_panel=self.curr_panel, addplot=self.plots)
    
    def add_study(self, study):
        data_points = study(self.data)

        for name, plot in study.plots.items():
            plot_type = plot['type'] if 'type' in plot else 'line'
            color = plot['color'] if 'color' in plot else 'blue'
            if study.lower:
                self.plots.append(mpf.make_addplot(data_points[name], panel=self.curr_panel, type=plot_type, color=color))
            else:
                self.plots.append(mpf.make_addplot(data_points[name], panel=0, type=plot_type, color=color))
        if study.lower:
            self.curr_panel += 1
        print("study added")

    def addplot(self, data, lower=False, plot_type='line', color='blue'):
        if lower:
            self.plots.append(mpf.make_addplot(data, panel=self.curr_panel, type=plot_type, color=color))
            self.curr_panel += 1
        else:
            self.plots.append(mpf.make_addplot(data, panel=0, type=plot_type, color=color))

    def __str__(self):
        return f"{self.ticker}"
