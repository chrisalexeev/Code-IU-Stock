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

    def full_sma(self,stock,days):
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

    def closing_sma_price(self,stock,days):
        vals = stock.close[-days]
        return sum(vals)/days

    def order_type(self, stock, account):
        """
        Check if stock should be bought or sold,
        and buys or sells it respectively
        """
        sma21 = self.closing_sma_price(stock,21)
        price = stock.price
        account_size = account.account_size
        current_trade = account.current_trade
        risk = account.risk

        # if price exceeds SMA and account is not currently buying, execute a buy
        if (price > sma21[-1]) and (current_trade != "Buy"):
            
            account.buy()

            for folder, history in account.running_trades.items():
                if folder == "Order_Type":
                    history.append("Buy")
                elif folder == "Order_Size":
                    history.append(self.order_size(account_size, price, risk))
                elif folder == "Price_Paid":
                    history.append(price)
                else:
                    pass
        
        # if price dips below SMA and account is not currently selling, execute a sell
        elif (price < sma21[-1]) and (current_trade != "Sell"): 

            account.sell()

            for folder, history in account.running_trades.items():
                if folder == "Order_Type":
                    history.append("Sell")
                elif folder == "Order_Size":
                    history.append(self.order_size(account_size, price, risk))
                    print(i)
                elif folder == "Price_Paid":
                    history.append(price)
                else:
                    pass