import numpy as np

class Study:
	def __init__(self):
		self.data = []

	def get_point(self, points, index):
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

	def get_point(self, points, index):
		average = 0
		if index >= self.period:
			# calculate sma
			if self.type == 'simple':
				if self.prev_val is None:
					for i in range(index-self.period, index):
						average += points[i]["Close"]/self.period
				else:
					average = self.prev_val - points[index-self.period]["Close"]/self.period + points[index]["Close"]/self.period
				self.prev_val = average
			# calculate ema
			elif self.type == 'exponential':
				if self.prev_val is None:
					for i in range(index-self.period, index):
						average += points[i]["Close"]/self.period
				else:
					average = points[index]["Close"]*self.smoothing + self.prev_val*(1-self.smoothing)
				self.prev_val = average
		else:
			average = np.nan

		return average