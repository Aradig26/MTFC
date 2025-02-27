import numpy as np
import pandas as pd
from pandas_datareader import data as wb
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class MonteCarlo():

    def __init__(self , ticker , start_date , end_date , days , sim):
        self.ticker = ticker
        self.start = start_date
        self.end = end_date
        self.noOfSimulations = sim
        self.noOfDays = days
        
        self.import_stock_data()
        self.calc_log_returns()
        self.volatility_calc()
        self.run_monteCarlo()
    
    def import_stock_data(self):
        self.data = pd.DataFrame()
    
        # Using Yahoo Finance to get stock data
        stock = yf.Ticker(ticker)
        self.data = stock.history(start=self.start)

    def calc_log_returns(self):

        # Using the 'Close' prices
        self.log_returns = np.log(1 + self.data['Close'].pct_change())
        self.log_returns = self.log_returns[1:]

    def volatility_calc(self):
        self.daily_volatility = np.std(self.log_returns)
    
    def run_monteCarlo(self):
        # Get the last days stock price
        last_price = self.data['Close'].iloc[-1]
        self.last_price = last_price
        
        # Initialize a list to store all simulation results
        all_simulations = []

        for x in range(self.noOfSimulations):
            price_series = [last_price]

            for y in range(1, self.noOfDays):
                price = price_series[-1] * (1 + np.random.normal(0, self.daily_volatility))
                price_series.append(price)

            all_simulations.append(price_series)

        # Convert the list of simulations into a DataFrame all at once
        self.simulation_df = pd.DataFrame(all_simulations).transpose()
                
    def results(self):
        # Extract the prices for the end of the second day (which is the last row in this case)
        prices = self.simulation_df.iloc[-1]  # Last row since num_days = 2

        # Calculate the 95% confidence interval
        lower_bound = np.percentile(prices, 2.5)
        upper_bound = np.percentile(prices, 97.5)

        # Calculate the mean (expected) price
        mean_price = np.mean(prices)

        # Print the results
        print(f"{self.ticker} expected price for {self.noOfDays} days later is: {mean_price} compared to the last price of {self.last_price}")
        print(f"{self.ticker} percent error is: {((mean_price - self.last_price) / self.last_price) * 100}%")
        print(f"{self.ticker} 95% confidence interval for the price {self.noOfDays} days later is: ({lower_bound}, {upper_bound})")
        print("\n")
        

# Define your list of tickers
tickers = ["GOOGL",	"AMZN",	"AAPL",	"BRK-A", "AVGO", "LLY", "JPM", "MA", "META", "MSFT", "NVDA", "^SPX", "TSLA", "UNH", "V", "WMT"]

end_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')  # Today's date in YYYY-MM-DD format
start_date = (datetime.now() - timedelta(days=10*365)).strftime('%Y-%m-%d')


# Initialize a dictionary to hold your results
results = {}

# Loop through each ticker and run the simulation
for ticker in tickers:
    simulation = MonteCarlo(ticker, start_date, end_date, (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days, 1000)
    simulation.results()



    