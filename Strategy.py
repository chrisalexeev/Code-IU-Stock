from Study import *
import numpy as np

# super basic right now
class Strategy:
  def __init__(self, stock, balance=10000):
    self.stock = stock
    self.stock_balance = 0
    self.cash_balance = balance
    self.position_size = 0

    self.bought = False
    self.sold = False
    self.data = Data()
  
  def buy(self, num, price):
    # prevent if we don't have enough money to buy
    if self.cash_balance < num*price: return

    self.bought = True
    self.position_size += num
    self.stock_balance += price*num
    self.cash_balance -= price*num
  
  def sell(self, num, price):
    # prevent if we have nothing to sell
    if self.position_size < num: return

    self.sold = True
    self.position_size -= num
    self.stock_balance -= price*num
    self.cash_balance += price*num

  def run(self):
    buys = []
    sells = []
    balances = []
    for i in range(len(self.stock.data)):
      # adjust the price of our stock balance from yesterday's close
      self.stock_balance += self.position_size * (self.stock.data["Open"][i]-self.stock.data["Close"][i-1])

      # buy or sell
      self.manage(i)

      # adjust the price of our stock balance from open to close
      self.stock_balance += self.position_size * (self.stock.data["Close"][i]-self.stock.data["Open"][i])

      # keeping track of buying and selling
      if self.bought: buys.append(True)
      else: buys.append(np.nan)
      if self.sold: sells.append(True)
      else: sells.append(np.nan)
      self.bought = False
      self.sold = False
      # keeping track of our total balance
      balances.append(self.cash_balance + self.stock_balance)

    # add all metrics we kept track of as data
    self.data.add_data('sells', sells)
    self.data.add_data('buys', buys)
    self.data.add_data('balance', balances)
      
  def manage(self, index):
    # can buy or sell here
    pass

  def getPL(self):
    return int(100 * (self.data['balance'][-1] - self.data['balance'][0]) / self.data['balance'][0])

class BuyAndHold(Strategy):
  def __init__(self, stock, balance=10000):
    super().__init__(stock, balance)

  def manage(self, index):
    if index == 0:
      # buy as much as we can
      self.buy(int(self.cash_balance/self.stock.data["Close"][index]), self.stock.data["Close"][index])

class MovingAverageCrossover(Strategy):
  def __init__(self, stock, balance=10000):
    super().__init__(stock, balance)
    self.shortMA = MovingAverage(period=12, type='exponential')
    self.shortMA = self.shortMA(self.stock.data)['average']
    self.longMA = MovingAverage(period=21, type='exponential')
    self.longMA = self.longMA(self.stock.data)['average']
  
  def manage(self, index):
    buy_amount = int(self.cash_balance/self.stock.data["Close"][index]) # using all of our cash

    if self.shortMA[index] > self.longMA[index] and self.shortMA[index-1] <= self.longMA[index-1]:
      self.buy(buy_amount, self.stock.data["Close"][index])
    if self.shortMA[index] < self.longMA[index] and self.shortMA[index-1] >= self.longMA[index-1]:
      self.sell(self.position_size, self.stock.data["Close"][index])
