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

	def get_close(self, price, index):
		return price[index]["Close"]

class MovingAverage(Study):
	def __init__(self, period=7, type='simple', param="Close"):
		super().__init__()
		self.period = period
		assert type in ['simple', 'exponential', 'wilders']
		self.type = type
		self.param = param

		# speeds up calculations
		self.prev_val = None

		# specific type stuff
		if self.type == 'simple':
			self.add_plot('average', self.get_simple)
		elif self.type == 'exponential':
			self.smoothing = 2/(self.period+1)
			self.add_plot('average', self.get_exponential)
		elif self.type == 'wilders':
			self.add_plot('average', self.get_wilders)

	def get_simple(self, price, index):
		average = 0
		if index >= self.period and not np.isnan(price[self.param][index-self.period]):
			# calculate sma
			if self.prev_val is None:
				for i in range(index-self.period, index):
					average += price[self.param][i]/self.period
			else:
				average = self.prev_val - price[self.param][index-self.period]/self.period + price[self.param][index]/self.period
			self.prev_val = average
		else:
			average = np.nan
		return average

	def get_exponential(self, price, index):
		average = 0
		if index >= self.period and not np.isnan(price[self.param][index-self.period]):
			# calculate ema
			if self.prev_val is None:
				for i in range(index-self.period, index):
						average += price[self.param][i]/self.period # the first value of the ema is an sma
			else:
				average = price[self.param][index]*self.smoothing + self.prev_val*(1-self.smoothing)
			self.prev_val = average
		else:
			average = np.nan
		return average

	def get_wilders(self, price, i):
		average = 0
		if i >= self.period and not np.isnan(price[self.param][i-self.period]):
			# calculate wma
			if self.prev_val is None:
				for i in range(i-self.period, i):
					average += price[self.param][i]/self.period # the first value of the wma is an sma
			else:
				average = price[self.param][i]/self.period + self.prev_val*(1 - 1/self.period)
			self.prev_val = average
		else:
			average = np.nan
		return average

class MACD(Study):
	def __init__(self, param="Close"):
		super().__init__()
		self.param = param
		self.shortEMA = MovingAverage(period=12, type='exponential', param=self.param).get_function()
		self.longEMA = MovingAverage(period=26, type='exponential', param=self.param).get_function()
		self.signalEMA = MovingAverage(period=9, type='exponential', param='macd').get_function()

		self.add_plot('macd', self.macd_line, color='blue')
		self.add_plot('signal', self.signal_line, color='red')
		self.add_plot('diff', self.diff_line, type='bar')
		self.add_plot('zero', self.zero_line)

		self.lower = True

	def zero_line(self, price, index):
		return 0

	def macd_line(self, price, index):
		short_point = self.shortEMA(price, index)
		long_point = self.longEMA(price, index)

		return short_point - long_point

	def signal_line(self, price, index):
		return self.signalEMA(self.data, index)

	def diff_line(self, price, index):
		return self.data['macd'][index] - self.data['signal'][index]

	def smooth(self, price, i):
		return self.moving_average(self.data, i)

class RSI(Study):
	def __init__(self, length=14, avg_type='wilders', param="Close"):
		super().__init__()
		self.lower = True
		self.length = length
		self.param = param

		self.gain_avg = MovingAverage(period=self.length, type=avg_type, param='gain').get_function()
		self.loss_avg = MovingAverage(period=self.length, type=avg_type, param='loss').get_function()

		self.add_plot('rsi', self.rsi)
	
	def rsi(self, points, i):
		# calculate gain/loss for the day
		price = points[self.param]
		self.data.add_point('gain', 0 if price[i]<price[i-1] or i==0 else price[i]-price[i-1])
		self.data.add_point('loss', 0 if price[i]>price[i-1] or i==0 else abs(price[i]-price[i-1]))

		# average gain/loss
		self.data.add_point('avg_gain', self.gain_avg(self.data, i))
		self.data.add_point('avg_loss', self.loss_avg(self.data, i))

		# relative strength and final RSI
		relative_strength = self.data['avg_gain'][i]/self.data['avg_loss'][i]
		return 100 - 100/(1+relative_strength)

class AverageTrueRange(Study):
	def __init__(self, length=12, avg_type='wilders'):
		super().__init__()
		self.lower = True
		self.moving_average = MovingAverage(length, avg_type, param='true_range').get_function()

		self.add_plot('atr', self.atr)

	def atr(self, price, i):
		self.data.add_point('true_range', self.true_range(price, i))

		return self.moving_average(self.data, i)

	def true_range(self, price, i):
		one = price["High"][i] - price["Low"][i]
		two = price["High"][i] - (np.nan if i==0 else price["Close"][i-1])
		three = (np.nan if i==0 else price["Close"][i-1]) - price["Low"][i]

		return max(one, max(two, three))

class SentimentZoneOscillator(Study):
	def __init__(self, length=14, param="Close"):
		super().__init__()
		self.lower = True
		self.length = length
		self.param = param

		self.ema1 = MovingAverage(period=self.length, type='exponential', param='sign').get_function()
		self.ema2 = MovingAverage(period=self.length, type='exponential', param='ema1').get_function()
		self.ema3 = MovingAverage(period=self.length, type='exponential', param='ema2').get_function()

		self.add_plot('szo', self.szo)
		self.add_plot('zero', self.zero, color='gray')

	def szo(self, price, i):
		self.data.add_point('sign', self.sign(price[self.param][i] - price[self.param][i-1]))

		# get ema of sign, then two more emas
		ema1 = self.ema1(self.data, i)
		self.data.add_point('ema1', ema1)
		ema2 = self.ema2(self.data, i)
		self.data.add_point('ema2', ema2)
		ema3 = self.ema3(self.data, i)

		# tema and szo final calculation
		tema = (ema1-ema2)*3 + ema3
		return 100 * tema / self.length

	def zero(self, price, i):
		return 0

	def sign(self, val):
		if val > 0: return 1
		elif val < 0: return -1
		return 0
