# main.py
# Regime Detection Starter Code

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    """Main function to run regime detection"""
    
    print("Downloading stock data...")
    
    # Download stock data (S&P 500 index)
    ticker = "SPY"  # S&P 500 ETF
    data = yf.download(ticker, start="2020-01-01", end="2024-01-01")
    
    print("Calculating returns and volatility...")
    
    # Calculate daily returns
    data['Returns'] = data['Close'].pct_change()
    
    # Calculate rolling volatility (20-day window)
    data['Volatility'] = data['Returns'].rolling(window=20).std()
    
    # Simple regime detection: High vol vs Low vol
    median_vol = data['Volatility'].median()
    data['Regime'] = data['Volatility'].apply(
        lambda x: 'High Volatility' if x > median_vol else 'Low Volatility'
    )
    
    print("Creating visualizations...")
    
    # Visualize
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot price
    ax1.plot(data.index, data['Close'])
    ax1.set_title(f'{ticker} Price')
    ax1.set_ylabel('Price ($)')
    
    # Plot volatility with regime coloring
    colors = {'High Volatility': 'red', 'Low Volatility': 'green'}
    for regime in data['Regime'].unique():
        regime_data = data[data['Regime'] == regime]
        ax2.scatter(regime_data.index, regime_data['Volatility'], 
                    c=colors[regime], label=regime, alpha=0.5, s=10)
    
    ax2.set_title('Volatility Regimes')
    ax2.set_ylabel('Volatility')
    ax2.legend()
    plt.tight_layout()
    plt.show()
    
    print("\nLast 10 days of data:")
    print(data[['Close', 'Returns', 'Volatility', 'Regime']].tail(10))
    
    print("\nRegime distribution:")
    print(data['Regime'].value_counts())

if __name__ == "__main__":
    main()