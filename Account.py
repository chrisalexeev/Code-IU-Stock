class Account:

    def __init__(self,acc_name,account_size=100000,risk=.02):
        self.name = acc_name
        self.account_size = 100000
        self.risk = .02

        # Calculate profit/loss and add it to account_size once trade is settled
        self.running_trades = {'Order_Type': [],
                                'Order_Size': [],
                                'Price_Paid': [],
                                'Close_Price': [],
                                'Profit':[]}

        # value of buy or sell used in order_type()
        self.current_trade = None

    # TODO: buy action
    def buy(self):
        self.current_trade = "Buy"

    # TODO: sell action
    def sell(self):
        self.current_trade = "Sell"