from SimpleStock import Stock
import Account
from Strategy import SMA_Strategy


if __name__ == "__main__":

    filename = "BABA.csv"
    baba = Stock("BABA",filename)

    baba.crude_graph()

    my_account = Account.Account("Chris's Account")

    test_strategy = SMA_Strategy()

    # print(sma21[-100:])

    test_strategy.order_type(baba,my_account)

    print(my_account.current_trade)

