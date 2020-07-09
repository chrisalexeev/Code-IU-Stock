from Study import *

# super basic right now
class Strategy:
  def __init__(self, stock, balance=10000):
    self.stock = stock
    self.start_balance = balance
    self.balance = balance
    self.position_size = 0
  
  def buy(self, num, price):
    self.balance -= num*price
    self.position_size += num
  
  def sell(self, num, price):
    self.balance += num*price
    self.position_size -= num

  def run(self):
    for i in range(len(self.stock.data)):
      self.manage(i)
      
  def manage(self, index):
    # can buy or sell here
    pass

  def getPL(self):
    return (self.balance + self.position_size*self.stock.data["Close"][-1] - self.start_balance) / self.start_balance

class BuyAndHold(Strategy):
  def __init__(self, stock, balance=10000):
    super().__init__(stock, balance)

  def manage(self, index):
    if index == 0:
      self.buy(10, self.stock.data["Close"][index])

class MovingAverageCrossover(Strategy):
  def __init__(self, stock, balance=10000):
    super().__init__(stock, balance)
    self.shortMA = MovingAverage(period=12, type='exponential')(self.stock.data)['average']
    self.longMA = MovingAverage(period=21, type='exponential')(self.stock.data)['average']
  
  def manage(self, index):
    if self.shortMA[index] > self.longMA[index] and self.shortMA[index-1] <= self.longMA[index-1]:
      self.sell(10, self.stock.data["Close"][index])
    if self.longMA[index] < self.shortMA[index] and self.longMA[index-1] <= self.shortMA[index-1]:
      self.buy(10, self.stock.data["Close"][index])

'''
How I (within reason) want a strategy to look like:

def __init__(self):
  self.baba = Stock("baba.csv")
  macd = MACD()
  average = MovingAverage(period=50, type='exponential' (param="Close"))

  self.diffValues = macd(baba)["diff"]
  self.longMa = average(baba)["average"]

def manage(self, index):
  if self.diffValues[index] > 0 and self.longMa.data[index] > baba.data["Close"][index]:
    self.buy(10, self.baba.data["Close"][index])

  if self.diffValues[index] < 0 and self.longMa.data[index] < baba.data["Close"][index]:
    self.sell(10, self.baba.data["Close"][index])
'''