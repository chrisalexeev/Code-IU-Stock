import numpy as np

class Study:
	def __init__(self):
		self.plots = []
		self.lower = False

	def __call__(self, points, index):
		return self.plots[0]['function'](points, index)

	def add_plot(self, func, **kwargs):
		kwargs['function'] = func
		self.plots.append(kwargs)

# example study
class GetClose(Study):
	def __init__(self):
		super().__init__()

		self.add_plot(self.get_close)

	def get_close(self, points, index):
		return points[index]["Close"]

class MovingAverage(Study):
	def __init__(self, period=7, type='simple'):
		super().__init__()
		self.period = period
		assert type in ['simple', 'exponential']
		self.type = type

		# speeds up calculations
		self.prev_val = None

		# specific type stuff
		if self.type == 'exponential':
			self.smoothing = 2/(self.period+1)
			self.add_plot(self.get_exponential)
		elif self.type == 'simple':
			self.add_plot(self.get_simple)

	def get_simple(self, points, index):
		average = 0
		if index >= self.period and not np.isnan(points[index-self.period]["Close"]):
			# calculate sma
			if self.prev_val is None:
				for i in range(index-self.period, index):
					average += points[i]["Close"]/self.period
			else:
				average = self.prev_val - points[index-self.period]["Close"]/self.period + points[index]["Close"]/self.period
			self.prev_val = average
		else:
			average = np.nan
		return average

	def get_exponential(self, points, index):
		average = 0
		if index >= self.period and not np.isnan(points[index-self.period]["Close"]):
			# calculate ema
			if self.prev_val is None:
				for i in range(index-self.period, index):
						average += points[i]["Close"]/self.period # the first value of the ema is a sma
						# print(points[i])
			else:
				average = points[index]["Close"]*self.smoothing + self.prev_val*(1-self.smoothing)
			self.prev_val = average
		else:
			average = np.nan
		return average

class MACD(Study):
	def __init__(self):
		super().__init__()
		self.shortEMA = MovingAverage(period=12, type='exponential')
		self.longEMA = MovingAverage(period=26, type='exponential')
		self.signalEMA = MovingAverage(period=9, type='exponential')

		self.macd = []
		self.signal = []

		self.add_plot(self.macd_line, color='blue')
		self.add_plot(self.signal_line, color='red')
		self.add_plot(self.diff_line, type='bar')
		self.add_plot(self.zero_line)

		self.lower = True

	def zero_line(self, points, index):
		return 0

	def macd_line(self, points, index):
		short_point = self.shortEMA(points, index)
		long_point = self.longEMA(points, index)

		self.macd.append({'Close': short_point-long_point})

		return short_point - long_point

	def signal_line(self, points, index):
		self.signal.append(self.signalEMA(self.macd, index))
		return self.signal[-1]

	def diff_line(self, points, index):
		return self.macd[index]["Close"] - self.signal[index]