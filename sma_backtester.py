import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def download_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)

    # Ensure Close column is a Series (handles multi-index cases)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
    if 'Close' not in data.columns:
        raise KeyError("No 'Close' price found in downloaded data.")

    data = data[['Close']].copy()
    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data.dropna(inplace=True)
    return data


def generate_signals(data, short_window=50, long_window=200):
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
    
    data['Signal'] = 0
    data.loc[data['SMA_short'] > data['SMA_long'], 'Signal'] = 1  # Long
    data['Position'] = data['Signal'].diff()
    return data


def backtest(data, initial_capital=10000):
    close_prices = data['Close'].squeeze()

    positions = pd.DataFrame(index=data.index)
    positions['Holdings'] = data['Signal'] * close_prices
    
    portfolio = pd.DataFrame(index=data.index)
    portfolio['Holdings'] = positions['Holdings']
    portfolio['Cash'] = initial_capital - (data['Position'] * close_prices).cumsum()
    portfolio['Total'] = portfolio['Cash'] + portfolio['Holdings']
    portfolio['Returns'] = portfolio['Total'].pct_change()
    return portfolio


def performance_metrics(portfolio):
    total_return = (portfolio['Total'][-1] / portfolio['Total'][0]) - 1
    win_trades = (portfolio['Returns'] > 0).sum()
    loss_trades = (portfolio['Returns'] < 0).sum()
    win_rate = win_trades / (win_trades + loss_trades) if (win_trades + loss_trades) > 0 else 0
    max_drawdown = (portfolio['Total'] / portfolio['Total'].cummax() - 1).min()
    
    metrics = {
        'Total Return (%)': round(total_return * 100, 2),
        'Win Rate (%)': round(win_rate * 100, 2),
        'Max Drawdown (%)': round(max_drawdown * 100, 2)
    }
    return metrics


def plot_results(data, portfolio):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Close'], label='Price', alpha=0.5)
    plt.plot(data['SMA_short'], label='Short SMA', alpha=0.7)
    plt.plot(data['SMA_long'], label='Long SMA', alpha=0.7)
    plt.plot(data[data['Position'] == 1].index, 
             data['SMA_short'][data['Position'] == 1], '^', markersize=10, color='g', label='Buy Signal')
    plt.plot(data[data['Position'] == -1].index, 
             data['SMA_short'][data['Position'] == -1], 'v', markersize=10, color='r', label='Sell Signal')
    plt.title('SMA Crossover Strategy')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2025-01-01"

    # Download and prepare data
    data = download_data(ticker, start_date, end_date)
    data = generate_signals(data, short_window=50, long_window=200)
    
    # Backtest
    portfolio = backtest(data)
    
    # Performance metrics
    metrics = performance_metrics(portfolio)
    print("\nPerformance Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")
    
    # Plot
    plot_results(data, portfolio)
