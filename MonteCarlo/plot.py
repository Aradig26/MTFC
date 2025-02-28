import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = "./monte_carlo_results.csv"  # Change this path if needed
df = pd.read_csv(file_path)

# Trim column names of whitespace
df.columns = df.columns.str.strip()

# Convert necessary columns to numeric, handling errors
df["Simulations"] = pd.to_numeric(df["Simulations"], errors="coerce")
df["Mean Price"] = pd.to_numeric(df["Mean Price"], errors="coerce")
df["Actual Price"] = pd.to_numeric(df["Actual Price"], errors="coerce")

# Drop any rows with missing values
df = df.dropna()

# Ensure numeric conversion after dropping NaNs
df["Simulations"] = df["Simulations"].astype(int)
df["Mean Price"] = df["Mean Price"].astype(float)
df["Actual Price"] = df["Actual Price"].astype(float)

# Get unique tickers
tickers = df["Ticker"].unique()

# Create a plot for each ticker
for ticker in tickers:
    ticker_data = df[df["Ticker"] == ticker]

    # Skip tickers with no valid data
    if ticker_data.empty:
        print(f"Skipping {ticker}: No valid data found.")
        continue

    plt.figure(figsize=(8, 5))
    plt.plot(ticker_data["Simulations"], ticker_data["Mean Price"], marker='o', linestyle='-', label="Mean Price")

    # Add text labels to each mean price point
    for i, row in ticker_data.iterrows():
        plt.text(row["Simulations"], row["Mean Price"], f"${row['Mean Price']:.2f}", 
                 fontsize=9, ha='right', va='bottom', color='blue')

    # Get the actual price safely
    actual_price = ticker_data["Actual Price"].iloc[0] if not ticker_data["Actual Price"].isna().all() else None

    if actual_price is not None:
        plt.axhline(actual_price, color='r', linestyle='--', label=f"Actual Price: {actual_price:.2f}")

    # Formatting
    plt.xscale("log")  # Log scale for simulations
    plt.xlabel("# of Simulations (Log Scale)")
    plt.ylabel("Price ($)")
    plt.title(f"{ticker} Monte Carlo Simulation Results")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)

    # Show the plot
    plt.show()
