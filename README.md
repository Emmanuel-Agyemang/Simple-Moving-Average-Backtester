## Simple Moving Average Backtester

A Python tool to backtest trading strategies using simple moving averages (SMA). Easily analyze historical stock data, visualize buy/sell signals, and evaluate performance.

---

## Features

- Fetch historical stock price data
- Compute simple moving averages (SMA)
- Generate buy/sell signals based on SMA crossovers
- Plot price data with SMA overlays and trade markers
- Evaluate strategy returns

---

## Usage Example

```python
from sma_backtester import SMABacktester

# Initialize backtester with stock ticker and SMA windows
backtester = SMABacktester(ticker='AAPL', short_window=40, long_window=100)

# Run backtest
backtester.run_backtest()

# Plot results with buy/sell signals
backtester.plot_results()
