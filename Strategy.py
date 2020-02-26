import math

class Strategy:
    def __init__(self):
        pass

    def order_size(self, account_size, price, risk):
        order = account_size * risk
        numOfStocks = math.floor(order/price)
        return numOfStocks 

class SMA_Strategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def simple_moving_avg(self,stock,days):
        """
        Create x day simple moving average data for given stock from close data
        """
        sma_close   = ['Close']
        val_list    = []
        sma_val     = 0
        first       = True

        for i,close in enumerate(stock.close):
            if i != 0:
                
                if i == days + 1: first = False
                if first:
                    sma_val += float(close)
                    sma_close.append(sma_val/i)
                    val_list.append(close)
                else:
                    val_list.append(close)
                    val_list = val_list[1:]
                    sma_val = sum(val_list)                    
                    sma_close.append(sma_val/days)      
        
        return sma_close

    def order_type(self,moving_avg_data, price, risk, account):
        """
        Check if stock should be bought or sold,
        and buys or sells it respectively
        """
        # if price exceeds SMA and account is not currently buying, execute a buy
        if (price > moving_avg_data[-1]) and (account.current_trade != "Buy"):
            
            account.buy()

            for x, y in account.running_trades.items():
                if x == "Order_Type":
                    y.append("Buy")
                elif x == "Order_Size":
                    y.append(self.order_size(account.account_size, price, account.risk))
                elif x == "Price_Paid":
                    y.append(price)
                else:
                    pass
        
        # if price dips below SMA and account is not currently selling, execute a sell
        elif (price < moving_avg_data[-1]) and (account.current_trade != "Sell"): 

            account.sell()

            for folder, history in account.running_trades.items():
                if folder == "Order_Type":
                    history.append("Sell")
                elif folder == "Order_Size":
                    history.append(self.order_size(account.account_size, price, account.risk))
                    print(i)
                elif folder == "Price_Paid":
                    history.append(price)
                else:
                    pass