import numpy as np
from Data import Data

class Study:
	def __init__(self):
		self.plots = {}
		self.data = Data()
		self.lower = False

	def __call__(self, datasource, params=None):
		for name, plot in self.plots.items():
			points = []
			for i in range(len(datasource)):
				points.append(plot['function'](datasource, i))
			self.data.add_data(plot['name'], points)
		return self.data

	# self.plots contains the functions, but also style attributes for drawing, like color
	def add_plot(self, name, func, **kwargs):
		kwargs['name'] = name
		kwargs['function'] = func
		self.plots[name] = kwargs

	def get_function(self, name=None):
		if name is None:
			return self.plots[list(self.plots.keys())[0]]['function'] # the first function
		else:
			return self.plots[name]['function']

# example study
class GetClose(Study):
	def __init__(self):
		super().__init__()

		self.add_plot('close', self.get_close)

	def get_close(self, points, index):
		return points[index]["Close"]

class MovingAverage(Study):
	def __init__(self, period=7, type='simple', param="Close"):
		super().__init__()
		self.period = period
		assert type in ['simple', 'exponential']
		self.type = type
		self.param = param

		# speeds up calculations
		self.prev_val = None

		# specific type stuff
		if self.type == 'exponential':
			self.smoothing = 2/(self.period+1)
			self.add_plot('average', self.get_exponential)
		elif self.type == 'simple':
			self.add_plot('average', self.get_simple)

	def get_simple(self, points, index):
		average = 0
		if index >= self.period and not np.isnan(points[self.param][index-self.period]):
			# calculate sma
			if self.prev_val is None:
				for i in range(index-self.period, index):
					average += points[self.param][i]/self.period
			else:
				average = self.prev_val - points[self.param][index-self.period]/self.period + points[self.param][index]/self.period
			self.prev_val = average
		else:
			average = np.nan
		return average

	def get_exponential(self, points, index):
		average = 0
		if index >= self.period and not np.isnan(points[self.param][index-self.period]):
			# calculate ema
			if self.prev_val is None:
				for i in range(index-self.period, index):
						average += points[self.param][i]/self.period # the first value of the ema is a sma
			else:
				average = points[self.param][index]*self.smoothing + self.prev_val*(1-self.smoothing)
			self.prev_val = average
		else:
			average = np.nan
		return average

class MACD(Study):
	def __init__(self):
		super().__init__()
		self.shortEMA = MovingAverage(period=12, type='exponential').get_function()
		self.longEMA = MovingAverage(period=26, type='exponential').get_function()
		self.signalEMA = MovingAverage(period=9, type='exponential', param='macd').get_function()

		self.add_plot('macd', self.macd_line, color='blue')
		self.add_plot('signal', self.signal_line, color='red')
		self.add_plot('diff', self.diff_line, type='bar')
		self.add_plot('zero', self.zero_line)

		self.lower = True

	def zero_line(self, points, index):
		return 0

	def macd_line(self, points, index):
		short_point = self.shortEMA(points, index)
		long_point = self.longEMA(points, index)

		return short_point - long_point

	def signal_line(self, points, index):
		return self.signalEMA(self.data, index)

	def diff_line(self, points, index):
		return self.data['macd'][index] - self.data['signal'][index]