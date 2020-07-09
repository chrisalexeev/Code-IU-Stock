class Strategy:
  def __init__(self):
    pass

'''
How I (within reason) want a strategy to look like:

def __init__(self):
  self.baba = Stock("baba.csv")
  macd = MACD()
  average = MovingAverage(period=50, type='exponential' (param="Close"))

  self.diffValues = macd(baba)["diff"]
  self.longMa = average(baba)["average"]

def buy(self, index):
  return self.diffValues[index] > 0 and self.longMa.data[index] > baba.data["Close"][index]

def sell(self, index):
  return self.diffValues[index] < 0 and self.longMa.data[index] < baba.data["Close"][index]
'''