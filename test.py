from Stock import Stock
from Study import *
from Strategy import BuyAndHold
from Strategy import MovingAverageCrossover

if __name__ == "__main__":
    baba = Stock("BABA", "BABA.csv")

    # add two moving average studies study
    baba.add_study(SentimentZoneOscillator())
    # baba.add_study(RSI())
    # baba.add_study(MovingAverage(12, 'simple'))
    # baba.add_study(MACD())

    # run strategies
    buy_and_hold = BuyAndHold(baba)
    ma_crossover = MovingAverageCrossover(baba)
    buy_and_hold.run()
    ma_crossover.run()

    # plot our balance over time and the buys and sells
    baba.addplot(ma_crossover.data['balance'], lower=True, plot_type='bar')
    # baba.addplot(ma_crossover.data['buys'], lower=False, plot_type='scatter', color='green')
    # baba.addplot(ma_crossover.data['sells'], lower=False, plot_type='scatter', color='red')

    print(str(buy_and_hold.getPL())+"%")
    print(str(ma_crossover.getPL())+"%")

    baba.plot()
