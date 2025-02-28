import numpy as np
import pandas as pd
import yfinance as yf
import statsmodels.api as sm

def fetch_data(symbol, start_date, end_date):
    """Fetch stock or index data, using Close price if Adj Close is missing."""
    data = yf.download(symbol, start=start_date, end=end_date)
    return data['Adj Close'] if 'Adj Close' in data else data['Close']

def calculate_beta(stock_symbol, market_symbol, start_date, end_date):
    """Calculate Beta using regression against market index returns."""
    stock_data = fetch_data(stock_symbol, start_date, end_date)
    market_data = fetch_data(market_symbol, start_date, end_date)

    if stock_data is None or market_data is None:
        return None

    # Calculate daily returns
    stock_returns = stock_data.pct_change().dropna()
    market_returns = market_data.pct_change().dropna()

    # Align data
    data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    data.columns = ['Stock', 'Market']

    # Run regression
    X = sm.add_constant(data['Market'])  
    model = sm.OLS(data['Stock'], X).fit()
    
    return model.params[1]  # Beta

def calculate_expected_return(rf, beta, rm):
    """Compute expected return using CAPM formula: E(R) = Rf + β(Rm - Rf)."""
    return rf + beta * (rm - rf)

# Example Parameters
rf = 0.03  # 3% risk-free rate
rm = 0.08  # 8% expected market return
stock_symbol = "AAPL"
market_symbol = "^GSPC" 
start_date = "2014-01-01"
end_date = "2024-01-01"

# Compute Beta & Expected Return
beta = calculate_beta(stock_symbol, market_symbol, start_date, end_date)

if beta is not None:
    expected_return = calculate_expected_return(rf, beta, rm)
    print(f"Beta: {beta:.2f}")
    print(f"Expected Return (CAPM): {expected_return:.2%}")
else:
    print("Error: Could not compute Beta.")