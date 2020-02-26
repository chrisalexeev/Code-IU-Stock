import pandas as pd

df = pd.read_csv("BABA.csv")

columns = ["Adj Close","Volume","High","Open","Low","Date"]

df.drop(columns, inplace=True, axis=1)

iterator = 21 #starting point
moving_avg = 0 #currently 21 days
Account_size = 100000
Risk = .02

# Calculate profit/loss and add it to account_size once trade is settled
running_trades =    {'Order_Type': [],
                    'Order_Size': [],
                    'Price_Paid': [],
                    'Close_Price': [],
                    'Profit':[]}

# value of buy or sell used in deforder_type
current_trade = None

#TODO It's supposed to start at the 21st value and take 21 day average
for i in df['Close'][iterator:]:
	moving_avg = df['Close'][iterator-21:iterator].mean() #takes mean of last 21 days
    
def order_size(Account_size, price, risk):
	x = Account_size * risk
	numOfStocks = round(x/price)
	return numOfStocks 

def order_type(moving_avg, price, risk, Account_size):
	if price > moving_avg:
		if current_trade == "Buy":
			pass
		else:
			#Settle the trade
			#calculate profit and add it to account_size
		for x, y in running_trades.items():
			if x == "Order_Type":
				y.append("Buy")
			elif x == "Order_Size":
				y.append(order_size(Account_size, i, Risk))
			elif x == "Price_Paid":
				y.append(price)
			else:
				pass
	elif price < moving_avg: 
		if current_trade == "Sell":
			pass
		else:
            pass
			#Settle the trade
			#calculate profit and add it to account_size
		for x, y in running_trades.items():
			if x == "Order_Type":
				y.append("Sell")
			elif x == "Order_Size":
				y.append(order_size(Account_size, i, Risk))
				print(i)
			elif x == "Price_Paid":
				y.append(price)
			else:
				pass
order_type(moving_avg, i, Risk, Account_size)
print(running_trades)