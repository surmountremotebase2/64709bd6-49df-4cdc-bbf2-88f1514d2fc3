from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, EMA, MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker we are interested in
        self.tickers = ["AAPL"]

    @property
    def assets(self):
        # Specifies which assets this strategy applies to
        return self.tickers

    @property
    def interval(self):
        # Defines the data interval; using daily data for this strategy
        return "1day"

    def run(self, data):
        # Initialize the stake for AAPL to 0
        aapl_stake = 0

        # Calculate the short-term (10 days) and long-term (40 days) moving averages
        short_term_sma = SMA("AAPL", data["ohlcv"], 10)
        long_term_sma = SMA("AAPL", data["ohlcv"], 40)

        # Ensure we have enough data points to calculate both SMAs
        if len(short_term_sma) > 0 and len(long_term_sma) > 0:
            current_price = data["ohlcv"][-1]["AAPL"]["close"]

            # Check for a bullish crossover; if it occurs, set the stake to 1
            if short_term_sma[-1] > long_term_sma[-1] and current_price > short_term_sma[-1]:
                log("Bullish crossover detected for AAPL - going long")
                aapl_stake = 1
            # Check for a bearish crossover; if it occurs, sell if we are holding 
            elif short_term_sma[-1] < long_term_sma[-1] and current_price < short_term_sma[-1]:
                log("Bearish crossover detected for AAPL - exiting position")
                aapl_stake = 0
            else:
                log("No clear trend detected for AAPL")

        # Return the target allocation as required by the Surmount trading package
        return TargetAllocation({"AAPL": aapl_stake})