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

    date = str(self.stock.data["Date"][self.current_index])
    self.data.add_point('activity', 'buy,'+date+','+str(num)+','+str(price))

    self.bought = True
    self.position_size += num
    self.stock_balance += price*num
    self.cash_balance -= price*num
  
  def sell(self, num, price):
    # prevent if we have nothing to sell
    if num > self.position_size or num == 0: return

    date = str(self.stock.data["Date"][self.current_index])
    self.data.add_point('activity', 'sell,'+date+','+str(num)+','+str(price))

    self.sold = True
    self.position_size -= num
    self.stock_balance -= price*num
    self.cash_balance += price*num

  def run(self):
    buys = []
    sells = []
    balances = []
    self.current_index = 0 # so we know which date we are on during buy/sell

    for i in range(len(self.stock.data)):
      # adjust the price of our stock balance from yesterday's close
      self.stock_balance += self.position_size * (self.stock.data["Open"][i]-self.stock.data["Close"][i-1])

      self.starting_position_size = self.position_size
      self.current_index = i
      # buy or sell
      self.manage(i)

      # adjust the price of our stock balance from open to close
      price_change = (self.stock.data["Close"][i]-self.stock.data["Open"][i])
      if self.bought == True or self.sold == True:
        self.stock_balance += self.starting_position_size * price_change
      else:
        self.stock_balance += self.position_size * price_change

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
    start_balance = self.data['balance'][0]
    end_balance = self.data['balance'][-1]
    return round(float(100 * (end_balance - start_balance) / start_balance), 2)

  # very crude right now
  def getWinPercent(self):
    activity = self.data['activity']
    last_buy_price = 0
    wins = 0
    trades = len(activity)/2
    for act in activity:
      data = act.split(',')
      if data[0] == 'buy':
        last_buy_price = float(data[3])
      else:
        price = float(data[3])
        if price > last_buy_price:
          wins += 1
    return wins/trades

class BuyAndHold(Strategy):
  def __init__(self, stock, balance=10000):
    super().__init__(stock, balance)

  def manage(self, index):
    if index == 0:
      # buy as much as we can
      self.buy(int(self.cash_balance/self.stock.data["Open"][index]), self.stock.data["Open"][index])

class MovingAverageCrossover(Strategy):
  def __init__(self, stock, balance=10000):
    super().__init__(stock, balance)
    self.shortMA = MovingAverage(period=12, type='exponential')
    self.shortMA = self.shortMA(self.stock.data)['average']
    self.longMA = MovingAverage(period=21, type='exponential')
    self.longMA = self.longMA(self.stock.data)['average']
  
  def manage(self, index):
    stock_price = self.stock.data["Close"][index]
    buy_amount = int(self.cash_balance/stock_price) # using all of our cash

    if self.shortMA[index] > self.longMA[index] and self.shortMA[index-1] <= self.longMA[index-1]:
      self.buy(buy_amount, stock_price)
    if self.shortMA[index] < self.longMA[index] and self.shortMA[index-1] >= self.longMA[index-1]:
      self.sell(self.position_size, stock_price)

class MACDCrossover(Strategy):
  def __init__(self, stock, balance=10000):
    super().__init__(stock, balance)
    self.macd = MACD()
    self.macd = self.macd(self.stock.data)

    self.diff = self.macd['diff']
    self.macd = self.macd['macd']

  def manage(self, i):
    stock_price = self.stock.data["Close"][i]
    buy_amount = int(self.cash_balance/stock_price) # using all of our cash

    if self.diff[i]>0 and self.diff[i-1]<=0:
      self.buy(buy_amount, stock_price)
    if self.diff[i]<0 and self.diff[i-1]>=0:
      self.sell(self.position_size, stock_price)

