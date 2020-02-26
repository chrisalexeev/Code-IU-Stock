import SimpleStock
import Account
from Strategy import SMA_Strategy


if __name__ == "__main__":

    filename = "BABA.csv"
    baba = SimpleStock.Stock("BABA",filename)

    my_account = Account.Account("Chris's Account")

    test_strategy = SMA_Strategy()

    sma21 = test_strategy.simple_moving_avg(baba,21)

    # print(sma21[-100:])

    test_strategy.order_type(sma21,baba.close[-1],0.2,my_account)

    print(my_account.current_trade)

