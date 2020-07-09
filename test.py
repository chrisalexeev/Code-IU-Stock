from Stock import Stock
from Study import MovingAverage
from Study import MACD
from Strategy import BuyAndHold
from Strategy import MovingAverageCrossover

if __name__ == "__main__":
    baba = Stock("BABA", "BABA.csv")

    # add two moving average studies study
    baba.add_study(MovingAverage(12, 'simple'))
    baba.add_study(MovingAverage(21, 'simple'))
    # baba.add_study(MACD())

    # run strategies
    buy_and_hold = BuyAndHold(baba)
    ma_crossover = MovingAverageCrossover(baba)
    buy_and_hold.run()
    ma_crossover.run()

    print(buy_and_hold.getPL())
    print(ma_crossover.getPL())

    baba.plot()
