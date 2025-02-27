import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_data():
    file_path = "MTFCDataMasterSheet.xlsx"
    df = pd.read_excel(file_path, sheet_name="DailyPrice")
    return df

# Get and print the table
df = get_data()


def monte_carlo_simulation(df, stock_name, num_simulations=10000):
    # Extract the AAPL price series
    aapl = df[stock_name]
    
    # Calculate log returns
    log_returns = np.log(aapl / aapl.shift(1)).dropna()
    
    # Split data: first half for training, second half for testing
    split_idx = len(log_returns) // 2
    train_returns = log_returns[:split_idx]
    test_returns = log_returns[split_idx:]

    # Monte Carlo parameters
    num_simulations = 10000
    num_days = len(test_returns)  # Simulate for the same period as test set

    # Get mean and standard deviation from training data
    mean_return = train_returns.mean()
    std_dev = train_returns.std()

    # Run Monte Carlo simulations
    np.random.seed(402)  # For reproducibility
    simulated_prices = np.zeros((num_simulations, num_days))
    last_train_price = aapl.iloc[split_idx]  # Last price from training set

    for i in range(num_simulations):
        daily_returns = np.random.normal(mean_return, std_dev, num_days)
        simulated_prices[i] = last_train_price * np.exp2(np.cumsum(daily_returns))  # Simulated price path

    # Compute the average simulated path
    average_simulated_path = simulated_prices.mean(axis=0)

    # Plot simulated paths
    plt.figure(figsize=(12, 6))
    # plt.plot(simulated_prices.T, alpha=0.1, color='blue', label="Monte Carlo Simulations")  # Monte Carlo paths
    plt.plot(average_simulated_path, color='green', linewidth=2, label="Average Simulated Price")  # Average path
    plt.plot(aapl[split_idx:].values, color='red', linewidth=2, label="Actual AAPL Prices")  # Actual test data
    plt.title("Monte Carlo Simulation for AAPL Stock Prices")
    plt.xlabel("Days")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.show()

    return simulated_prices, test_returns

# Call the function
simulated_prices, test_returns = monte_carlo_simulation(df, "AAPL", 9023949)
print(simulated_prices.std().mean())
print(test_returns.get_values().std())  